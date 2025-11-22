from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView,ListAPIView
from api.permission import IsAuthAndDone,IsAuthDoneAndOwner
from api.serializers import CreatePostSerialzer,DeletePostSerialzer,MyPostsSerialzer,PostsLikeSeriazlier
from api.models import Post,User
from api.utils import MyResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Post"])
class CreatePost(APIView):
    permission_classes=[IsAuthAndDone]
    serializer_class=CreatePostSerialzer
    def post(self,request):
        try:
            user=User.objects.get(username=request.user.username)
            serializer=self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
        except:
            return MyResponse.error("Invalid data was entered")
        

        Post.objects.create(user=user,content=serializer.validated_data.get("content"))
        return MyResponse.success(
            message="Post created seccessfully",
            data=user.username
        )
 
@extend_schema(tags=["Post"])
class DeletePost(DestroyAPIView):
    queryset=Post.objects.all()
    serializer_class=DeletePostSerialzer
    permission_classes=[IsAuthDoneAndOwner ,]

@extend_schema(tags=["Post"])
class AllMyPosts(APIView):
    serializer_class = MyPostsSerialzer
    permission_classes = [IsAuthDoneAndOwner]

    def get(self, request):
        user = request.user
        posts = Post.objects.filter(user=user)

        serializer = self.serializer_class(posts, many=True)

        return MyResponse.success(serializer.data)
      
@extend_schema(tags=["Post"])
class GetMyPost(APIView):
    serializer_class = MyPostsSerialzer
    permission_classes = [IsAuthDoneAndOwner]

    def get(self, request, pk):
        user = request.user
        try:
          post = get_object_or_404(Post, user=user, pk=pk)
        except:
            return MyResponse.error(f"There isn't your post with this id :{pk}")

        serializer = self.serializer_class(post)

        return MyResponse.success(serializer.data)
    

@extend_schema(tags=["Likes"])
class Like_to_Post(APIView):
    serializer_class=PostsLikeSeriazlier
    def post(self,request,pk):
            try:
                user=User.objects.get(username=request.user.username)
                post=Post.objects.get(pk=pk)
                if post.liked_user.filter(id=user.id).exists():
                    return MyResponse.error("You have already liked the post")
                post.liked_user.add(user)
                post.save()
                serializer=self.serializer_class(post)
            except:
                return MyResponse.error("invalid data was entered")
            
            return MyResponse.success(
            message="Post liked successfully",
            data=serializer.data)
    
    permission_classes=[IsAuthDoneAndOwner]
    def delete(self,request,pk):
        try:
            user=User.objects.get(username=request.user.username)
            post=Post.objects.get(pk=pk)
            if not post.liked_user.filter(id=user.id).exists():
                return MyResponse.error("You have already deleted like from the post")
            post.liked_user.remove(user)
            post.save()
            serializer=self.serializer_class(post)
        except:
            return MyResponse.error("Invalid data was entered")
        
        return MyResponse.success(
        message="Your like successfully deleted from the post",
        data=serializer.data)

@extend_schema(tags=["Likes"])
class AllMyLikes(ListAPIView):
    serializer_class = PostsLikeSeriazlier
    permission_classes = [IsAuthAndDone]

    def get_queryset(self):
        user = self.request.user
        return MyResponse.success(
            message="All your liked posts",
            data =Post.objects.filter(liked_user=user))



@extend_schema(tags=["Views"])
class Post_View(APIView):
    serializer_class=PostsLikeSeriazlier
    permission_classes=[IsAuthAndDone]
    def post(self,request,pk):
            try:
                user=User.objects.get(username=request.user.username)
                post=Post.objects.get(pk=pk)
                if post.viewed_user.filter(id=user.id).exists():
                    return MyResponse.error("You have already viewed the post")
                post.viewed_user.add(user)
                post.save()
                serializer=self.serializer_class(post)
            except:
                return MyResponse.error("invalid data was entered")
            
            return MyResponse.success(
            message="Post viewed successfully",
            data=serializer.data)

@extend_schema(tags=["Views"])
class AllMyViews(ListAPIView):
    serializer_class = PostsLikeSeriazlier
    permission_classes = [IsAuthAndDone]

    def get_queryset(self):
        user = self.request.user
        return MyResponse.success(
            message="All your viewed posts",
            data =Post.objects.filter(viewed_user=user))

   
    
    



