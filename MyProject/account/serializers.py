from rest_framework import serializers

from rest_framework import exceptions
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from account.models import Account
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email', '')
        password = data.get('password', '')
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    data['user'] = user

                else:
                    msg = 'This user has been deactivated by admin PLeace COntact with admin or make a new account'
                    raise exceptions.ValidationError(msg)
            else:
                msg = 'It is not possible login with this info'
                exceptions.ValidationError(msg)
        else:
            msg = 'Password and Username is necessasary!'
            raise exceptions.ValidationError(msg)

        data['tokens'] = user.tokens()
        return data


class RegistrationSerilaizer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'})

    def validate_email(self, email):
        existing = Account.objects.filter(email=email).first()
        if existing:
            raise serializers.ValidationError(
                "Someone with that email "
                "address has already registered. Was it you?")

        return email

    def validate(self, data):
        if not data.get('password'):  # or not data.get('password2'):
            raise serializers.ValidationError("Please enter a password and "
                                              "confirm it.")
        return data

    def create(self, validated_data):

        return Account.objects.create_user(username=validated_data['username'],
                                           email=validated_data['email'],
                                           password=validated_data['password'])


class emailVerifySerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=550)

    class Meta:
        model = Account
        fields = ['token']


class resetPasswordRequestEmailSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(min_length=3)

    class Meta:
        model = Account
        fields = ['email']


class passwordRequestEmailVerify(serializers.ModelSerializer):
    token = serializers.CharField(min_length=4)


class setNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ['password']

    def validate(self, attrs):
        try:
            uidb64 = attrs.get('uidb64')
            token = attrs.get('token')
            password = attrs.get('password')
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthorizationFailded(
                    'Token is not valid please order new One Fuck Trump', 401)

            user.set_password(password)
            user.save()
            return user
        except DjangoUnicodeDecodeError:
            raise AuthorizationFailded(
                'Token is not valid please order new One Fuck Trump', 401)
        return super().validate(attrs)
