from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from django.contrib import admin
from django.urls import path, include
from .views import (GenericAPIViews, ArticleListDetailView, ArticleDetailView,
                    ArticleListCreateView, ArticleView)

urlpatterns = [
    path('article/', ArticleListCreateView.as_view(), name='article-list'),
    path('article/<int:id>',
         ArticleListDetailView.as_view(),
         name='article-detail'),
    path('accounts/', include('account.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns += [
#         static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     ]
