from django.contrib import admin
from image_cropping import ImageCroppingMixin

from .models import Category, Topic, User_info, Post_info, Relationship, Comments, Like, Message, Favourite

# Register your models here.

admin.site.register(Category),
admin.site.register(Topic),
admin.site.register(User_info),
admin.site.register(Post_info),
admin.site.register(Relationship),
admin.site.register(Comments),
admin.site.register(Like),
admin.site.register(Message),
admin.site.register(Favourite),
