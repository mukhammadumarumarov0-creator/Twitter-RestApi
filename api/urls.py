from django.urls import path
from .views import SendEmailCodeApiView,VerificationApiView,ResentCodeApiView,UpdateVerifedUserApiView,LoginUserApiView,\
   GetChangePasswordToken,PasswordUpdateView,CreatePost,DeletePost,AllMyPosts,GetMyPost,CreateComent,CommentDetail,\
   AllMyComments,PostComments

urlpatterns = [
    # Auth
   path("sign-up/",SendEmailCodeApiView.as_view()),
   path("verification/",VerificationApiView.as_view()),
   path("resend_code/",ResentCodeApiView.as_view()),
   path("update_user/",UpdateVerifedUserApiView.as_view()),
   path("login_user/",LoginUserApiView.as_view()),
   path("password_token/",GetChangePasswordToken.as_view()),
   path("change_password/",PasswordUpdateView.as_view()),

   # Post
  path("create_post/",CreatePost.as_view()),
  path("delete_post/<int:pk>",DeletePost.as_view()),
  path("all_posts/",AllMyPosts.as_view()),
  path("post/<int:pk>",GetMyPost.as_view()),

  # Comment
  path("create_comment/",CreateComent.as_view()),
  path("all_my_comments/",AllMyComments.as_view()),
  path("posts_comment/<int:pk>",PostComments.as_view()),
  path("comment_detail/<int:pk>/",CommentDetail.as_view()),



]
