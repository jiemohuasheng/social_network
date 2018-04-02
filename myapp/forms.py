from django import forms
from myapp.models import User_info, Category, Topic, Post_info, Comments, Like


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User_info
        fields = ['first_name', 'last_name', 'username', 'email', 'user_sec_ques', 'user_sec_ans', 'user_dob_month',
                  'user_dob_date', 'user_dob_year', 'password', 'user_country', 'user_city', 'user_pic']
        widgets = {'password': forms.PasswordInput(), }


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User_info
        fields = ['first_name', 'last_name', 'email', 'user_country', 'user_city', 'user_web_url', 'user_pic']



class LoginForm(forms.ModelForm):
    class Meta:
        model = User_info
        fields = ['email', 'password']
        widgets = {'password': forms.PasswordInput()}



class ForgotPassword(forms.ModelForm):
    class Meta:
        model = User_info
        fields = ['username', 'password']


class PasswordChangeForm(forms.ModelForm):
    class Meta:
        model = User_info
        fields = ['password']

class AboutMeInfoForm(forms.ModelForm):
    class Meta:
        model = User_info
        fields = ['user_abtme_desc', 'user_abtme_title']


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post_info
        fields = ['post_title', 'post_desc', 'post_file', 'post_disp_img', 'post_video_url', 'tags']
        labels= {'post_title':'Post Title', 'post_desc':'Post Description', 'post_file':'Upload Files',
                 'post_disp_img':'Cover Image', 'post_video_url':'Embed media','tags':'Add Tags'}
        widgets = {'post_desc': forms.Textarea}


class AddCommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = {'comm_desc'}


class AddLikesForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ['like_post', 'like_user']