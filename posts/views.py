import requests
import os

from dotenv import load_dotenv

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Post, Comment
from .serializers import PostSerializer, PostDetailSerializer, RatingSerializer, \
    CommentSerializer
from .permissions import IsPostOwnerOrStaff

load_dotenv()

class PostView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
class AddPostView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsPostOwnerOrStaff]  

    def perform_create(self, serializer):
        post = serializer.save(user=self.request.user)  
        self.send_telegram_message(post.user.telegram, f"Ваш пост успешно опубликован.")

    def send_telegram_message(self, chat_id, message):
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        url = f'https://api.telegram.org/bot{token}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': message
        }
        requests.post(url, data=payload)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsPostOwnerOrStaff]

class CommentView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class AddCommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsPostOwnerOrStaff]

class RatingView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id') 
        post = generics.get_object_or_404(Post, id=post_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post, auth=request.user)


        post.refresh_from_db()
        post_serializer = PostDetailSerializer(post)  

        return Response(post_serializer.data, status=status.HTTP_201_CREATED)
