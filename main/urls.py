"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from users.views import RegisterView
from posts.views import PostView, RatingView, AddPostView, PostDetailView, \
    CommentView, AddCommentView

urlpatterns = [
    path('admin/', admin.site.urls),

    #users
    path('api/acсount/register/', RegisterView.as_view(), name='register'),
    path('api/account/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    #posts
    path('api/post/', PostView.as_view(), name='post'),
    path('api/post_add/', AddPostView.as_view(), name='post_add'),
    path('api/post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('api/post/<int:pk>/comment/', CommentView.as_view(), name='comment'),
    path('api/post/<int:pk>/comment_add/', AddCommentView.as_view(), name='comment_add'),
    path('api/post/<int:post_id>/mark_add/', RatingView.as_view(), name='mark_add'),
]
