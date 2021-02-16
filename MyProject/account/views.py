from django.shortcuts import render


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
