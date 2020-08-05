# Generated by Django 3.1 on 2020-08-05 12:07

import buyer.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                (
                    'last_login',
                    models.DateTimeField(
                        blank=True, null=True, verbose_name='last login'
                    ),
                ),
                (
                    'is_superuser',
                    models.BooleanField(
                        default=False,
                        help_text='Designates that this user has all permissions without explicitly assigning them.',
                        verbose_name='superuser status',
                    ),
                ),
                (
                    'first_name',
                    models.CharField(
                        blank=True, max_length=150, verbose_name='first name'
                    ),
                ),
                (
                    'last_name',
                    models.CharField(
                        blank=True, max_length=150, verbose_name='last name'
                    ),
                ),
                (
                    'is_staff',
                    models.BooleanField(
                        default=False,
                        help_text='Designates whether the user can log into this admin site.',
                        verbose_name='staff status',
                    ),
                ),
                (
                    'date_joined',
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name='date joined'
                    ),
                ),
                (
                    'is_active',
                    models.BooleanField(
                        default=False,
                        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
                        verbose_name='active',
                    ),
                ),
                (
                    'email',
                    models.EmailField(
                        help_text='Primary identifier.',
                        max_length=254,
                        unique=True,
                        verbose_name='email address',
                    ),
                ),
                (
                    'groups',
                    models.ManyToManyField(
                        blank=True,
                        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                        related_name='user_set',
                        related_query_name='user',
                        to='auth.Group',
                        verbose_name='groups',
                    ),
                ),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[('objects', buyer.models.UserManager()),],
        ),
        migrations.CreateModel(
            name='ResetToken',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('token', models.CharField(max_length=64)),
                ('used', models.BooleanField(default=False)),
                ('expires_on', models.DateTimeField(default=buyer.models.tomorrow)),
                (
                    'buyer',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='tokens',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('city', models.CharField(max_length=50)),
                ('pin_code', models.CharField(max_length=7)),
                ('house_number', models.CharField(max_length=50)),
                (
                    'state',
                    models.CharField(
                        choices=[
                            ('AP', 'Andhra Pradesh'),
                            ('AR', 'Arunachal Pradesh'),
                            ('AS', 'Assam'),
                            ('BR', 'Bihar'),
                            ('CG', 'Chhattisgarh'),
                            ('GA', 'Goa'),
                            ('GJ', 'Gujarat'),
                            ('HR', 'Haryana'),
                            ('HP', 'Himachal Pradesh'),
                            ('JK', 'Jammu and Kashmir'),
                            ('JH', 'Jharkhand'),
                            ('KA', 'Karnataka'),
                            ('KL', 'Kerala'),
                            ('MP', 'Madhya Pradesh'),
                            ('MH', 'Maharashtra'),
                            ('MN', 'Manipur'),
                            ('ML', 'Meghalaya'),
                            ('MZ', 'Mizoram'),
                            ('NL', 'Nagaland'),
                            ('OR', 'Orissa'),
                            ('PB', 'Punjab'),
                            ('RJ', 'Rajasthan'),
                            ('SK', 'Sikkim'),
                            ('TN', 'Tamil Nadu'),
                            ('TR', 'Tripura'),
                            ('UK', 'Uttarakhand'),
                            ('UP', 'Uttar Pradesh'),
                            ('WB', 'West Bengal'),
                            ('AN', 'Andaman and Nicobar Islands'),
                            ('CH', 'Chandigarh'),
                            ('DH', 'Dadra and Nagar Haveli'),
                            ('DD', 'Daman and Diu'),
                            ('DL', 'Delhi'),
                            ('LD', 'Lakshadweep'),
                            ('PY', 'Pondicherry'),
                        ],
                        help_text='Delivery address state.',
                        max_length=2,
                    ),
                ),
                (
                    'buyer',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='addresses',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={'verbose_name': 'Address', 'verbose_name_plural': 'Addresses',},
        ),
        migrations.AddField(
            model_name='buyer',
            name='primary_address',
            field=models.ForeignKey(
                blank=True,
                help_text='Primary address to deliver items to.',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='primary_buyer',
                to='buyer.address',
            ),
        ),
        migrations.AddField(
            model_name='buyer',
            name='user_permissions',
            field=models.ManyToManyField(
                blank=True,
                help_text='Specific permissions for this user.',
                related_name='user_set',
                related_query_name='user',
                to='auth.Permission',
                verbose_name='user permissions',
            ),
        ),
        migrations.AddIndex(
            model_name='address',
            index=models.Index(fields=['buyer'], name='buyer_addre_buyer_i_85d365_idx'),
        ),
    ]
