from rest_framework import serializers
from .models import Article
from rest_framework import exceptions
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from account.models import Account
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'author',
            'slug',
            'image',
            'date_published',
            'date_updated',
        ]


# def create(self, validated_data):

#     print('validated_data', validated_data)
#     user = Account.objects.create_user(username=validated_data['username'],
#                                        email=validated_data['email'],
#                                        password=validated_data['password'])
#     # user.set_password(validated_data['password'])
#     # user.save()
#     return user

# class RegistrationSerilaizer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True,
#                                      style={'input_type': 'password'})

#     class Meta:
#         model = Account
#         fields = [
#             'email',
#             'username',
#             'password',
#         ]
#         extra_kwargs = {'password': {'write_only': True}}
#         read_only_fields = ['password2']

#         def create(self, validated_data):
#             print('*************************************', validated_data)
#             last_validation = validated_data.pop('password2')
#             user = Account(username=validated_data['username'],
#                            email=validated_data['email'],
#                            password=validated_data['password'])
#             user.set_password(password)
#             user.save()
#             return user

# def save(self):
#     validated_data = validated_data.pop('password2')
#     print('validated_data', validated_data)
#     user = Account(username=self.validated_data['username'],
#                    email=self.validated_data['email'])
#     password = self.validated_data['password']

#     password2 = self.validated_data['password2']
#     if password != password2:
#         raise serializers.ValidationError(
#             'passwords dont match with each other')
#     user.set_password(password)
#     user.save()
#     return user

# class ArticleSerializer(serializers.Serializer):

# title=serializers.CharField(max_length=100)
# author=serializers.CharField(max_length=100)
# emai=serializers.EmailField(max_length=100)
# date=serializers.DateTimeField()

# def create(self,validated_data):
#     return Article.objects.create(validated_data)
# def update(self, instance, validated_data):
#     instance.title=validated_data.get('title', instance.title)
#     instance.author=validated_data.get('author',instance.author)
#     instance.emai=validated_data.get('emai'.instance.emai)
#     instance.date=validated_data.get('date',instance.date)
#     instance.save()
#     return instance
