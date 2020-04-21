from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse ,JsonResponse
from rest_framework.parsers  import JSONParser
from .models import  Article
from .serializers import ArticleSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class GenericAPIViews(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class=ArticleSerializer
    queryset=Article.objects.all()
    lookup_field='id'
    authentication_classes=[SessionAuthentication, BasicAuthentication]
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self, request, id=None): 
        if id:
            return self.retrieve(request,id)

        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)
    def put(self, request, id=None):
        return self.update(request, id)
    def delete(self, request, id=None):
        return self.destroy(request, id)





class ArticleView(APIView):


    def get(self, request):
        articles=Article.objects.all()
        serializer=ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=ArticleSerializer(data=request.data)
        #request.POST  # Only handles form data.  Only works for 'POST' method.
        #request.data  # Handles arbitrary data.  Works for 'POST', 'PUT' and 'PATCH' methods.
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error, status.HTTP_400_BAD_REQUEST)


class ArticleDetailView(APIView):
    def get(self, request, pk):
        try:
           article= Article.objects.get(pk=pk)
        except: 
            return HttpResponse(status.HTTP_404_NOT_FOUND)
        
        serializer= ArticleSerializer(article)
        return Response(serializer.data)
    def put(self, request, pk):
        article=Article.objects.get(pk=pk)
        serializer=ArticleSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request, pk):
        article=Article.objects.get(pk=pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# Create your views here.

# @api_view(['GET', 'POST'])
# def article_list(request):
#     if request.method=='GET':
#         articles=Article.objects.all()
#         serializer=ArticleSerializer(articles, many=True)
#         return Response(serializer.data)

#     elif request.method=='POST':
       
#         serializer=ArticleSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','PUT', 'DELETE'])
# @csrf_exempt
# def article_detail(request,pk):
#     try:
#         article=Article.objects.get(pk=pk)
#     except:
#         return HttpResponse(status.HTTP_404_NOT_FOUND)
    
#     if  request.method=='GET':
#         serializer=ArticleSerializer(article)
#         return Response(serializer.data)
#     elif request.method=='PUT':
#         #data=JSONParser().parse(request)
#         serializer=ArticleSerializer(article, data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method=='DELETE':
#         article.delete()
#         return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)




