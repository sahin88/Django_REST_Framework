from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from django.contrib import admin
from django.urls import path, include
from .views import (GenericAPIViews, LoginView, ArticleListDetailView, ArticleDetailView,
                    ArticleView, LogoutView, alist, adetail, registration, verifyEmail, resetPasswordRequestEmail, ArticleListCreateView, passwordRequestEmailVerify, setNewPassword,)


urlpatterns = [
    path('article/', ArticleListCreateView.as_view(), name='article-list'),
    path('article/<int:id>', ArticleListDetailView.as_view(), name='article-detail'),
    path('logout/', LogoutView.as_view()),
    path('register/', registration, name='regist'),
    path('login/', LoginView.as_view(), name='logins'),
    path('email-verify/', verifyEmail.as_view(), name='email-verify'),
    path('reset-email-request/', resetPasswordRequestEmail.as_view(),
         name='reset-email-request'),
    path('reset-email-verify/<uidb64>/<token>/',
         passwordRequestEmailVerify.as_view(), name='reset-email-verify'),
    path('reset-email-complete/',
         setNewPassword.as_view(), name='reset-email-complete'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns += [
#         static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     ]
