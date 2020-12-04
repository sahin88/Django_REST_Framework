from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Article
from account.models import Account
from .serializers import ArticleSerializer, LoginSerializer, RegistrationSerilaizer, emailVerifySerializer, resetPasswordRequestEmailSerializer, setNewPasswordSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .permissions import IsOwner


class ArticleListCreateView(ListCreateAPIView):

    article = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwner,
    )

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)


class ArticleListDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)
    lookup_field = 'id'

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)


class AricleViewSets(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'id'


# class ApiViewSet(viewsets.Viewset):
#     def list(self, request):
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = ArticleSerializer(data=request.data)
#         # request.POST  # Only handles form data.  Only works for 'POST' method.
#         # request.data  # Handles arbitrary data.  Works for 'POST', 'PUT' and 'PATCH' methods.
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.error, status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request):
#         queryset = Article.objects.all()
#         article = get_object_or_404(queryset, pk=pk)
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)


class GenericAPIViews(generics.GenericAPIView, mixins.ListModelMixin,
                      mixins.CreateModelMixin, mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated, IsAdminUser]
    # authentication_classes = [TokenAuthentication]

    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)

        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id=None):
        return self.destroy(request, id)


def get_actual_value(request):
    if request.user is None:
        return None

    return request.user  # here should have value, so any code using request.user will work


class MyCustomMiddleware(object):
    def process_request(self, request):
        request.custom_prop = SimpleLazyObject(
            lambda: get_actual_value(request))


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        print('request', request.data)

        serialized_data = LoginSerializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        user = serialized_data.validated_data['user']

        django_login(request, user)
        # token, created = Token.objects.get_or_create(user=user)
        # print('login_tokenm', serialized_data.validated_data['tokens'])
        return Response({'token': serialized_data.validated_data['tokens']},
                        status=status.HTTP_200_OK)


class LogoutView(APIView):
    authentication_classes = [
        TokenAuthentication,
    ]

    def post(self, request):
        django_logout(request)
        return Response(status=204)


class ArticleView(APIView):
    authentication_classes = (TokenAuthentication)

    def get(self, request):

        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        # request.POST  # Only handles form data.  Only works for 'POST' method.
        # request.data  # Handles arbitrary data.  Works for 'POST', 'PUT' and 'PATCH' methods.
        if serializer.is_valid():
            serializer.save(raise_exception=True)
            return Response(serializer.data)
        return Response(serializer.error, status.HTTP_400_BAD_REQUEST)


class ArticleDetailView(APIView):
    def get(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
            artee = Article.objects.filter(pk=pk)
            print('#Sansür', article.author, artee[0].author,
                  self.request.user, self.request.user)
        except:
            return HttpResponse(status.HTTP_404_NOT_FOUND)

        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        article = Article.objects.get(pk=pk)
        serializer = ArticleSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = Article.objects.get(pk=pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Create your views here.


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes([TokenAuthentication])
def alist(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def adetail(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except:
        return HttpResponse(status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # data=JSONParser().parse(request)
        serializer = ArticleSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        article.delete()
        return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)


class verifyEmail(APIView):

    serializer_class = emailVerifySerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            paylooad = jwt.decode(token, settings.SECRET_KEY)
            user = Account.objects.get(id=paylooad['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response('data: you  have been succesfully verified',
                            status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifer:
            Response('error: Activation has not been done',
                     status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifer:
            Response('error: Activation has not been done',
                     status=status.HTTP_400_BAD_REQUEST)


@api_view([
    'POST',
])
def registration(request):

    serializer = RegistrationSerilaizer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        user = Account.objects.get(email=serializer.data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain

        relativeLink = reverse('email-verify')

        abslurl = 'http://' + current_site + relativeLink + '?token=' + str(
            token)

        email_body = 'Hi'+user.username + \
            'Please verify your account via provided link' + abslurl
        data = {
            'email_body': email_body,
            'subject': 'Verify your email adress',
            'to_email': user.email
        }
        Util.send_email(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class resetPasswordRequestEmail(generics.GenericAPIView):
    serializer_class = resetPasswordRequestEmailSerializer

    def post(self, request):
        # serializer = self.requestPasswordResetEmailSerializer(
        #     data=request.data)
        # serializer.is_verified(raise_exception=True)
        print('request', request.data['email'])

        if Account.objects.filter(email=request.data['email']).exists():
            user = Account.objects.get(email=request.data['email'])
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('reset-email-verify',
                                   kwargs={
                                       'token': token,
                                       'uidb64': uidb64
                                   })
            abslurl = 'http://' + current_site + relativeLink
            print('abslurl', abslurl)
            email_body = 'Hi'+user.username + \
                'Please verify your account via provided link' + abslurl
            data = {
                'email_body': email_body,
                'subject': 'Verify your email adress',
                'to_email': user.email
            }
            Util.send_email(data)
        return Response('Status: EMail  has been sucessfully send to  user',
                        status=status.HTTP_200_OK)


class passwordRequestEmailVerify(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    'Token is not valid please order new One Fuck Trump',
                    status=status.HTTP_401_UNAUTHORIZED)
            return Response({
                'Sucess': True,
                'message': 'Crendential is ok',
                'token': token,
                'uidb64': uidb64
            })
        except DjangoUnicodeDecodeError as identifier:
            Response({'errors': identifer})


class setNewPassword(generics.GenericAPIView):
    serializer_class = setNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                'Sucess': True,
                'message': 'Password has been sucessfully changed'
            },
            status=status.HTTP_200_OK)
