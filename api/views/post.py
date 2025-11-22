from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView
from api.permission import IsAuthAndDone,IsAuthDoneAndOwner
from api.serializers import CreatePostSerialzer,DeletePostSerialzer,MyPostsSerialzer
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
    

