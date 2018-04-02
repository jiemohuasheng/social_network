from django.db import models
from django.contrib.auth.models import User
from image_cropping import ImageRatioField
from taggit.managers import TaggableManager
from taggit.models import CommonGenericTaggedItemBase, TaggedItemBase




# Create your models here.

class Topic(models.Model):
    topic_name = models.CharField(max_length=100, default=None)
    topic_choices = (
        ('Health', 'Health'),
        ('Education', 'Education'),
        ('Funny', 'Funny')
    )
    topic_type = models.CharField(max_length=100, choices=topic_choices, default='Health')

    def __str__(self):
        return self.topic_type


class Category(models.Model):
    cat_choices = (
        ('Videos','video'),
        ('Pictures','picture'),
        ('Gifs','gif')
    )
    cat_type = models.CharField(choices=cat_choices, max_length=10, default='Videos')
    cat_file = models.FileField(upload_to='images', default=None, blank=None)
    cat_top = models.ForeignKey(Topic, default=None, on_delete=None)

    def __str__(self):
        return self.cat_type


class User_info(User):
    user_country = models.CharField(max_length=20, default=None, blank=True, null=True)
    user_city = models.CharField(max_length=20, default=None, blank=True, null=True)
    user_sec_ques = models.CharField(max_length=60, default=None, blank=True, null=True)
    user_sec_ans = models.CharField(max_length=60, default=None, blank=True, null=True)
    user_dob_month = models.CharField(max_length=60, default=None, blank=True, null=True)
    user_dob_date = models.CharField(max_length=60, default=None, blank=True, null=True)
    user_dob_year = models.CharField(max_length=60, default=None, blank=True, null=True)
    user_pic = models.ImageField(upload_to='', default='default_user.jpg', blank=True, null=True)
    user_pic_crop = ImageRatioField('user_pic', '400x400')
    user_web_url = models.CharField(max_length=50, default=None, blank=True, null=True)
    user_abtme_title = models.CharField(max_length=20, default=None, blank=True, null=True)
    user_abtme_desc = models.CharField(max_length=200, default=None, blank=True, null=True)
    user_relationship = models.ManyToManyField('self', through='Relationship',
                                               symmetrical=False, related_name='related_to')
    def __str__(self):
        return self.username


RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_FOLLOWING_SELF = 3
RELATIONSHIP_STATUS = (
    (RELATIONSHIP_FOLLOWING, 'Following'),
    (RELATIONSHIP_BLOCKED, 'Blocked'),
    (RELATIONSHIP_FOLLOWING_SELF, 'Following Self')
)


class Relationship(models.Model):
    rel_from_user = models.ForeignKey(User_info, related_name='from_user', on_delete=None)
    rel_to_user = models.ForeignKey(User_info, related_name='to_user', on_delete=None)
    rel_status = models.IntegerField(choices=RELATIONSHIP_STATUS)

    def __str__(self):
        return str(self.rel_from_user)+ ' '+str(self.rel_status)+ ''+ str(self.rel_to_user)


class GenericStringTaggedItem(CommonGenericTaggedItemBase, TaggedItemBase):
    object_id = models.CharField(max_length=50, verbose_name=('Object id'), db_index=True)

class Post_info(models.Model):
    post_title = models.CharField(max_length=200, default=None, blank=True, null=True)
    post_desc = models.CharField(max_length=5000, default=None, blank=True, null=True)
    post_file = models.FileField(upload_to='', default=None, blank=True, null=True)
    post_user = models.ForeignKey(User_info, default=None, on_delete=None)
    post_disp_img = models.ImageField(upload_to='', default=None, blank=True, null=True)
    post_publish_date = models.DateField(default=None, blank=True, null=True)
    post_publish_time = models.TimeField(default=None, blank=True, null=True)
    post_video_url = models.CharField(max_length=200, default=None, blank=True, null=True)
    tags = TaggableManager(through=GenericStringTaggedItem)

    def __str__(self):
        return self.post_title


class Comments(models.Model):
    comm_desc = models.CharField(max_length=2000, default=None, blank=True, null=True)
    comm_publish_date = models.DateField(default=None, blank=True, null=True)
    comm_publish_time = models.TimeField(default=None, blank=True, null=True)
    comm_user = models.ForeignKey(User_info, default=None, on_delete=None)
    comm_post = models.ForeignKey(Post_info, default=None, on_delete=None)



class Like(models.Model):
    like_user = models.ForeignKey(User_info, default=None, on_delete=None)
    like_post = models.ForeignKey(Post_info, default=None, on_delete=None)


class Favourite(models.Model):
    fav_user = models.ForeignKey(User_info, default=None, on_delete=None)
    fav_post = models.ForeignKey(Post_info, default=None, on_delete=None)


class Message(models.Model):
    msg_sender = models.ForeignKey(User_info, related_name='msg_sender', on_delete=None)
    msg_reciever = models.ForeignKey(User_info, related_name='msg_reciever', on_delete=None)
    msg_content = models.CharField(max_length=500, default=None)
    msg_publish_date = models.DateField(default=None, blank=True, null=True)
    msg_publish_time = models.TimeField(default=None, blank=True, null=True)




