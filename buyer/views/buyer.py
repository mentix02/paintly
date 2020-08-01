from django.conf import settings

from rest_framework import status
from google.oauth2 import id_token
from rest_framework.views import APIView
from google.auth.transport import requests
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from buyer.tasks import send_reset_email
from buyer.models import Buyer, ResetToken


class BuyerChangePasswordAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        data = {'error': True, 'message': ''}
        try:
            old_password = request.POST['old_password']
            new_password = request.POST['new_password']
        except KeyError as field:
            data['message'] = f'{field} not provided.'
        else:
            if len(new_password) <= 8:
                data['message'] = 'Password must be greater than 8 characters.'
            else:
                buyer = request.user
                if buyer.check_password(old_password):
                    buyer.set_password(new_password)
                    buyer.save()
                    data['error'] = False
                    data['message'] = 'Password changed successfully.'
                else:
                    data['message'] = 'Incorrect password provided.'
        finally:
            return Response(
                data,
                status=status.HTTP_400_BAD_REQUEST
                if data['error']
                else status.HTTP_200_OK,
            )


class BuyerActivateAPIView(APIView):
    @staticmethod
    def post(request):
        data = {'error': True, 'message': ''}
        token = request.POST.get('token')
        if token is not None:
            try:
                t = Token.objects.get(key__exact=token)
            except Token.DoesNotExist:
                data['message'] = 'Invalid auth token provided.'
            else:
                buyer = t.user
                buyer.is_active = True
                buyer.save()
                data['error'] = False
                data['message'] = 'Activated account.'
        else:
            data['message'] = 'Authentication token not provided.'
        return Response(
            data,
            status=status.HTTP_400_BAD_REQUEST if data['error'] else status.HTTP_200_OK,
        )


class BuyerRegisterAPIView(APIView):
    @staticmethod
    def post(request):
        data = {'error': True, 'message': ''}
        try:
            email = request.POST['email']
            name = request.POST['name']
            password = request.POST['password']
        except KeyError as field:
            data['message'] = f'{str(field)} not provided.'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        try:
            Buyer.objects.get(email__iexact=email)
        except Buyer.DoesNotExist:
            buyer = Buyer.objects.create_user(email=email, password=password)
            buyer.set_full_name(name)
            data['error'] = False
            data['message'] = 'Registered successfully.'
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data['message'] = f'User with email {email} exists.'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class BuyerSendPasswordResetLinkAPIView(APIView):

    """ Sends a password reset link with auth_token to buyer for resetting account password. """

    @staticmethod
    def post(request):

        data = {
            'error': False,
            'message': 'Email containing reset link was sent.',
        }

        email = request.POST.get('email')

        if email is not None:
            try:
                buyer = Buyer.objects.get(email__iexact=email)
            except Buyer.DoesNotExist:
                # Just send back a success response if phony email was provided.
                return Response(data)
            else:
                token = buyer.generate_reset_token()
                send_reset_email.delay(buyer.email, token.token)
        else:
            data['error'] = True
            data['message'] = 'Email not provided.'

        return Response(data)


class ValidateResetTokenAPIView(APIView):

    """ Validates auth_token keys validity. """

    @staticmethod
    def post(request):
        data = {'error': True, 'message': ''}
        token = request.POST.get('token')
        if token is not None:
            valid, _ = ResetToken.valid_token(token)
            if not valid:
                data['message'] = 'Invalid reset token provided.'
            else:
                data['error'] = False
                data['message'] = 'Valid token.'
        else:
            data['message'] = 'Reset token not provided.'
        return Response(
            data,
            status=status.HTTP_400_BAD_REQUEST if data['error'] else status.HTTP_200_OK,
        )


class BuyerResetPasswordAPIView(APIView):

    """ Requires a valid auth_token key for user and resets with provided password. """

    @staticmethod
    def post(request):
        data = {'error': True, 'message': 'Invalid token provided.'}

        try:
            # Get data.
            token = request.POST['token']
            password = request.POST['password']

        except KeyError as field:
            # Return missing field error message.
            data['message'] = f'{str(field)} not provided.'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        else:

            # Query for reset token.
            valid: bool
            rt: ResetToken
            valid, rt = ResetToken.valid_token(token)

            if not valid:
                data['message'] = 'Invalid reset token provided.'
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            # User token and set password.
            buyer = rt.buyer
            buyer.set_password(password)
            buyer.save()
            rt.use()

            # Return success response.
            data['error'] = False
            data['message'] = 'Password reset successfully.'
            return Response(data)


class GoogleSignInAPIView(APIView):
    @staticmethod
    def post(request):
        token = request.POST.get('token')
        if token is None:
            return Response(
                {'error': 'Token not provided.'}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), settings.GOOGLE_OAUTH2_KEY
            )
            if idinfo['iss'] not in [
                'accounts.google.com',
                'https://accounts.google.com',
            ]:
                return Response(
                    {'error': 'Wrong issuer.'}, status=status.HTTP_400_BAD_REQUEST
                )
            buyer, created = Buyer.objects.get_or_create(
                is_active=True, email__iexact=idinfo.pop('email'),
            )

            if created:
                buyer.last_name = idinfo.pop('family_name')
                buyer.first_name = idinfo.pop('given_name')
                buyer.save()

            return Response(
                {'token': buyer.auth_token.key},
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
            )
        except ValueError:
            return Response(
                {'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST
            )
