from django.contrib import admin
from api.models.user import User,UserConfirmation,ChangeUsersPassword
from api.models.post import Post,Media
from api.models.comment import Comment

admin.site.register([User,UserConfirmation,Post,Media,Comment,ChangeUsersPassword])
