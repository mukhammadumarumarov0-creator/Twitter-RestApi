from rest_framework.views import APIView
from api.permission import IsAuthAndDone,IsAuthDoneAndOwner
from api.models import Comment,User,Post
from api.serializers import CommentSerializer,CommentInDetailSerializer
from api.utils import MyResponse
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Comments"])
class CreateComent(APIView):
    permission_classes=[IsAuthAndDone ,]
    serializer_class=CommentSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        user=User.objects.get(username=request.user.username)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        print(serializer)

        return MyResponse.success(
            "Comment created successfully"
        )


@extend_schema(tags=["Comments"])
class AllMyComments(APIView):
    serializer_class=CommentInDetailSerializer
    permission_classes = [IsAuthAndDone]
    def get(self,request):
        try:
          user=User.objects.get(username=request.user.username)
          comments=Comment.objects.filter(user=user)
          serializer=self.serializer_class(comments,many=True)
        except:
            return MyResponse.error("error was occured")
        return MyResponse.success(
            message="User's all comments",
            data=serializer.data
        )


@extend_schema(tags=["Comments"])
class PostComments(APIView):
    permission_classes=[IsAuthAndDone ,]
    serializer_class=CommentInDetailSerializer

    def get(self,request,pk):
        try:
          post=Post.objects.get(pk=pk)
          p_comment=Comment.objects.filter(post=post)
          serializer=self.serializer_class(p_comment,many=True)
        except:
            return MyResponse.error("Invalid data was entered")
        return MyResponse.success(
            message="Post all comments",
            data=serializer.data
        )


@extend_schema(tags=["Comments"])
class CommentDetail(RetrieveUpdateDestroyAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    permission_classes = [IsAuthDoneAndOwner]



        




