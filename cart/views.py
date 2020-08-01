from typing import Dict, Tuple, Union

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from cart.models import CartItem
from cart.serializers import CartItemSerializer


def _is_num(n: str) -> bool:
    try:
        int(n)
    except ValueError:
        return False
    else:
        return True


def _process_cart_item(
    request,
) -> Union[
    Tuple[Dict[str, Union[bool, str]], CartItem],
    Tuple[Dict[str, Union[bool, str]], None],
]:
    data = {'error': True}
    cart_item_id = request.POST.get('cart_item_id')
    if cart_item_id is not None and _is_num(cart_item_id):
        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
        except CartItem.DoesNotExist:
            data['message'] = 'Invalid cart item id provided.'
        else:
            data['error'] = False
            return data, cart_item
    else:
        data['message'] = 'Cart item id not provided.'
    return data, None


def _mutate_cart_item(request, delta: int) -> Response:

    data: Dict[str, Union[bool, str]]
    cart_item: CartItem

    data, cart_item = _process_cart_item(request)

    if not data['error']:
        cart_item.quantity += delta
        data['error'] = False
        if cart_item.quantity == 0:
            data['message'] = 'Cart item removed.'
            cart_item.delete()
        else:
            if delta >= 0:
                data['message'] = 'Cart item quantity incremented.'
            else:
                data['message'] = 'Cart item quantity decremented.'
            cart_item.save()
    return Response(
        data,
        status=status.HTTP_400_BAD_REQUEST if data['error'] else status.HTTP_200_OK,
    )


class RemoveCartItemAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request) -> Response:
        data, cart_item = _process_cart_item(request)
        if not data['error']:
            cart_item.delete()
            data['error'] = False
            data['message'] = 'Deleted cart item.'
        return Response(
            data,
            status=status.HTTP_400_BAD_REQUEST if data['error'] else status.HTTP_200_OK,
        )


class DecrementCartItemQuantity(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request) -> Response:
        return _mutate_cart_item(request, -1)


class IncrementCartItemQuantity(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request) -> Response:
        return _mutate_cart_item(request, 1)


class AddCartItemAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request) -> Response:
        data = {'error': True}
        painting_id = request.POST.get('painting_id')
        if painting_id is not None and _is_num(painting_id):
            request.user.cart.add(int(painting_id))
            data['error'] = False
            data['message'] = f'Added {painting_id} to cart.'
        else:
            data['message'] = 'Painting ID not provided.'
        return Response(
            data,
            status=status.HTTP_400_BAD_REQUEST
            if data['error']
            else status.HTTP_201_CREATED,
        )


class CartItemListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartItemSerializer

    def get_queryset(self):
        qs = self.request.user.cart.items.all()
        qs.prefetch_related('painting')
        return qs
