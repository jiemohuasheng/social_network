from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils import timezone
import datetime



from myapp.forms import RegisterForm, LoginForm, ForgotPassword, PasswordChangeForm, UserInfoForm, AboutMeInfoForm, \
    AddPostForm, AddCommentsForm, AddLikesForm
from myapp.models import User_info, Post_info, Topic, Relationship, Comments, Like, Message, Favourite
from django.contrib.auth import update_session_auth_hash



@login_required(login_url="/myapp/login/", redirect_field_name='')
def index(request):
    user_p = get_object_or_404(User_info, id=request.user.id)
    post_d = user_p.post_info_set.order_by('id')
    get_post = Post_info.objects.order_by('-id')[:5]
    base_post = Post_info.objects.order_by('-id') [:10]

    post_dt = Post_info.objects.all().distinct().order_by('-id')
    user_r = user_p.user_relationship.filter(to_user__rel_status=1)
    user_s = user_p.user_relationship.filter(to_user__rel_status=3)
    user_t = user_r|user_s
    if request.method == 'POST':
        if 'srch' in request.POST:
            gt_post = Post_info.objects.filter(
                    post_title__startswith=request.POST.get('username')
                    )

            get_user = User_info.objects.filter(
                username=request.POST.get('username')
            ) or User_info.objects.filter(
                    first_name=request.POST.get('username')
                    ) or User_info.objects.filter(
                    last_name=request.POST.get('username')
                    ) or User_info.objects.filter(
                user_city=request.POST.get('username')

            ) or User_info.objects.filter(
                user_country=request.POST.get('username')
            )

            return render(request, 'myapp/explore.html', {'user_p': user_p,
                                                          'post_d': post_d,
                                                          'get_user': get_user,
                                                          'gt_post': gt_post,
                                                          'base_post': base_post
                                                          })
    return render(request, 'myapp/index.html', {'user_p': user_p,
                                                'post_dt': post_dt,
                                                'user_r': user_r,
                                                'post_d': post_d,
                                                'user_t': user_t,
                                                'get_post': get_post,
                                                'base_post': base_post
                                                })


@login_required(login_url="/myapp/login/", redirect_field_name='')
def my_prof(request):
    user = get_object_or_404(User_info, id=request.user.id)
    followers = user.related_to.all().count()-1
    following = user.user_relationship.all().count()-1
    post_data = user.post_info_set.order_by('-id')
    user_r = user.user_relationship.filter(to_user__rel_status=1)
    post_dt = Post_info.objects.filter(post_user__to_user__rel_status=1).distinct()
    p_d = Relationship.objects.filter(rel_from_user__user_relationship__post_info=1)
    user_f = user.related_to.filter(from_user__rel_status=1)
    fav_usr = user.favourite_set.all()

    base_post = Post_info.objects.order_by('-id') [:10]


    return render(request, 'myapp/myprofile.html', {'post_data': post_data,
                                                    'user': user,
                                                    'followers': followers,
                                                    'following': following,
                                                    'user_r': user_r,
                                                    'user_f': user_f,
                                                    'post_dt': post_dt,
                                                    'p_d': p_d,
                                                    'fav_usr': fav_usr,
                                                    'base_post': base_post
                                                    })


@login_required(login_url="/myapp/login/", redirect_field_name='')
def explore_viw(request):
    user = get_object_or_404(User_info, id=request.user.id)
    post_data = Post_info.objects.order_by('-id', '-post_publish_date', '-post_publish_time')
    base_post = Post_info.objects.order_by('-id') [:10]

    if request.method == 'POST':
        if 'srch' in request.POST:
            get_post = Post_info.objects.filter(
                    post_title__startswith=request.POST.get('username')
                    )

            get_user = User_info.objects.filter(
                username=request.POST.get('username')
            ) or User_info.objects.filter(
                    first_name=request.POST.get('username')
                    ) or User_info.objects.filter(
                    last_name=request.POST.get('username')
                    ) or User_info.objects.filter(
                user_city=request.POST.get('username')

            ) or User_info.objects.filter(
                user_country=request.POST.get('username')
            )

            return render(request, 'myapp/explore.html', {'user': user,
                                                          'post_data': post_data,
                                                          'get_user': get_user,
                                                          'get_post': get_post,
                                                          'base_post': base_post
                                                          })

    return render(request, 'myapp/explore.html', {'user': user,
                                                  'post_data': post_data,
                                                  'base_post': base_post
                                                  })



@login_required(login_url="/myapp/login/", redirect_field_name='')
def user_prof(request, id):
    user = get_object_or_404(User_info, id=request.user.id)
    user_prf = get_object_or_404(User_info, id=id)
    post_data = user_prf.post_info_set.order_by('-id', '-post_publish_date', '-post_publish_time')
    followers = user_prf.related_to.all().count()-1
    following = user_prf.user_relationship.all().count()-1
    followers_u = str(user.related_to.all())
    following_u = user.user_relationship.filter(to_user__rel_status=1)
    user_1 = User_info.objects.get(id=request.user.id)
    user_2 = user_prf
    user_f = user.related_to.filter(from_user__rel_status=1)
    like_pst = user_prf.like_set.all().count()
    base_post = Post_info.objects.order_by('-id') [:10]

    if request.method == 'POST':
        if 'add_rel' in request.POST:
            Relationship.objects.get_or_create(
                rel_from_user=user_1,
                rel_to_user=user_2,
                rel_status=1
            )
            return render(request, 'myapp/userprofile.html', {'user_prf': user_prf,
                                                      'user': user,
                                                      'followers': followers,
                                                      'following': following,
                                                      'post_data': post_data,
                                                      'following_u': following_u,
                                                      'followers_u': followers_u,
                                                      'user_f': user_f,
                                                          'base_post': base_post,
                                                              'like_pst': like_pst
                                                      })
        if 'del_rel' in request.POST:
            Relationship.objects.filter(
                rel_from_user=user_1,
                rel_to_user=user_2,
                rel_status=1
            ).delete()
            return render(request, 'myapp/userprofile.html', {'user_prf': user_prf,
                                                      'user': user,
                                                      'followers': followers,
                                                      'following': following,
                                                      'post_data': post_data,
                                                      'following_u': following_u,
                                                      'followers_u': followers_u,
                                                      'user_f': user_f,
                                                          'base_post': base_post,
                                                              "like_pst": like_pst
                                                              })

    return render(request, 'myapp/userprofile.html', {'user_prf': user_prf,
                                                      'user': user,
                                                      'followers': followers,
                                                      'following': following,
                                                      'post_data': post_data,
                                                      'following_u': following_u,
                                                      'followers_u': followers_u,
                                                      'user_f': user_f,
                                                          'base_post': base_post,
                                                      'like_pst': like_pst
                                                      })



@login_required(login_url="/myapp/login/", redirect_field_name='')
def postdetail_viw(request, id):
    user = get_object_or_404(User_info, id=request.user.id)
    user_3 = User_info.objects.filter(id=request.user.id)
    followers = str(user.related_to.all())
    postdet = get_object_or_404(Post_info, id=id)
    comments = Comments.objects.all()
    c = postdet.comments_set.count()
    following = user.user_relationship.filter(to_user__rel_status=1)
    user_1 = User_info.objects.get(id=request.user.id)
    user_2 = postdet.post_user
    form = AddCommentsForm()
    likes = Like.objects.all().distinct()
    like_user = postdet.like_set.filter(like_user=request.user)
    like_usr = user.like_set.all()
    likes_count = postdet.like_set.count()
    fav = Favourite.objects.all().distinct()
    fav_user = postdet.favourite_set.all()
    fa_user = postdet.favourite_set.filter(fav_user=request.user)
    fav_count = postdet.favourite_set.count()
    user_f = user.related_to.filter(from_user__rel_status=1)
    base_post = Post_info.objects.order_by('-id') [:10]

    if request.method == 'POST':
        if 'del_pst' in request.POST:
            Comments.objects.filter(comm_post=postdet).delete()
            Like.objects.filter(like_post=postdet).delete()
            Favourite.objects.filter(fav_post=postdet).delete()
            get_object_or_404(Post_info, id=id).delete()
            return HttpResponseRedirect('/myapp/myprofile/')

        if 'add_rel' in request.POST:
            Relationship.objects.get_or_create(
                rel_from_user=user_1,
                rel_to_user=user_2,
                rel_status=1
            )
            return render(request, 'myapp/postdetail.html', {'user': user,
                                                     'postdet': postdet,
                                                     'followers': followers,
                                                     'following': following,
                                                     'user_1': user_1,
                                                     'user_2': user_2,
                                                     'user_3': user_3,
                                                     'comments': comments,
                                                     'likes': likes,
                                                     'likes_count': likes_count,
                                                     'c': c,
                                                     'like_user': like_user,
                                                     'user_f': user_f,
                                                     'fav': fav,
                                                     'fav_count': fav_count,
                                                     'fav_user': fav_user,
                                                     'fa_user': fa_user,
                                                          'base_post': base_post
                                                     })

        if 'del_rel' in request.POST:
            Relationship.objects.filter(
                rel_from_user=user_1,
                rel_to_user=user_2,
                rel_status=1
            ).delete()
            return render(request, 'myapp/postdetail.html', {'user': user,
                                                     'postdet': postdet,
                                                     'followers': followers,
                                                     'following': following,
                                                     'user_1': user_1,
                                                     'user_2': user_2,
                                                     'user_3': user_3,
                                                     'comments': comments,
                                                     'likes': likes,
                                                     'likes_count': likes_count,
                                                     'c': c,
                                                     'like_user': like_user,
                                                     'user_f': user_f,
                                                     'fav': fav,
                                                     'fav_count': fav_count,
                                                     'fav_user': fav_user,
                                                     'fa_user': fa_user,
                                                          'base_post': base_post
                                                     })

        if 'add_comment' in request.POST:
            form = AddCommentsForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.comm_desc = request.POST.get('comm_desc')
                comment.comm_publish_date = timezone.now()
                comment.comm_publish_time = datetime.datetime.now()
                comment.comm_user = user
                comment.comm_post = postdet
                comment.save()
                return render(request, 'myapp/postdetail.html', {'user': user,
                                                             'postdet': postdet,
                                                             'followers': followers,
                                                             'following': following,
                                                             'user_1': user_1,
                                                             'user_2': user_2,
                                                             'user_3': user_3,
                                                             'comments': comments,
                                                             'likes': likes,
                                                             'likes_count': likes_count,
                                                             'c': c,
                                                             'like_user': like_user,
                                                             'user_f': user_f,
                                                             'fav': fav,
                                                             'fav_count': fav_count,
                                                             'fav_user': fav_user,
                                                             'fa_user': fa_user,
                                                          'base_post': base_post
                                                             })

        if 'add_like' in request.POST:
            Like.objects.get_or_create(
                like_user = user,
                like_post = postdet
            )
            return render(request, 'myapp/postdetail.html', {'user': user,
                                                             'postdet': postdet,
                                                             'followers': followers,
                                                             'following': following,
                                                             'user_1': user_1,
                                                             'user_2': user_2,
                                                             'user_3': user_3,
                                                             'comments': comments,
                                                             'likes': likes,
                                                             'likes_count': likes_count,
                                                             'c': c,
                                                             'like_user': like_user,
                                                             'user_f': user_f,
                                                             'fav': fav,
                                                             'fav_count': fav_count,
                                                             'fav_user': fav_user,
                                                             'fa_user': fa_user,
                                                          'base_post': base_post
                                                             })

        if 'del_like' in request.POST:
            Like.objects.filter(
                like_user = user,
                like_post = postdet
            ).delete()
            return render(request, 'myapp/postdetail.html', {'user': user,
                                                             'postdet': postdet,
                                                             'followers': followers,
                                                             'following': following,
                                                             'user_1': user_1,
                                                             'user_2': user_2,
                                                             'user_3': user_3,
                                                             'comments': comments,
                                                             'likes': likes,
                                                             'likes_count': likes_count,
                                                             'c': c,
                                                             'like_user': like_user,
                                                             'user_f': user_f,
                                                             'fav': fav,
                                                             'fav_count': fav_count,
                                                             'fav_user': fav_user,
                                                             'fa_user': fa_user,
                                                          'base_post': base_post
                                                             })

        if 'add_fav' in request.POST:
            Favourite.objects.get_or_create(
                fav_user = user,
                fav_post = postdet
            )
            return render(request, 'myapp/postdetail.html', {'user': user,
                                                             'postdet': postdet,
                                                             'followers': followers,
                                                             'following': following,
                                                             'user_1': user_1,
                                                             'user_2': user_2,
                                                             'user_3': user_3,
                                                             'comments': comments,
                                                             'likes': likes,
                                                             'likes_count': likes_count,
                                                             'c': c,
                                                             'like_user': like_user,
                                                             'user_f': user_f,
                                                             'fav': fav,
                                                             'fav_count': fav_count,
                                                             'fav_user': fav_user,
                                                             'fa_user': fa_user,
                                                          'base_post': base_post
                                                             })

        if 'del_fav' in request.POST:
            Favourite.objects.filter(
                fav_user=user,
                fav_post=postdet
            ).delete()
            return render(request, 'myapp/postdetail.html', {'user': user,
                                                             'postdet': postdet,
                                                             'followers': followers,
                                                             'following': following,
                                                             'user_1': user_1,
                                                             'user_2': user_2,
                                                             'user_3': user_3,
                                                             'comments': comments,
                                                             'likes': likes,
                                                             'likes_count': likes_count,
                                                             'c': c,
                                                             'like_user': like_user,
                                                             'user_f': user_f,
                                                             'fav': fav,
                                                             'fav_count': fav_count,
                                                             'fav_user': fav_user,
                                                             'fa_user': fa_user,
                                                          'base_post': base_post
                                                             })

    else:
        return render(request, 'myapp/postdetail.html', {'user': user,
                                                         'postdet': postdet,
                                                         'followers': followers,
                                                         'following': following,
                                                         'user_1': user_1,
                                                         'user_2': user_2,
                                                         'user_3': user_3,
                                                         'comments': comments,
                                                         'form': form,
                                                         'c':c,
                                                         'likes': likes,
                                                         'likes_count': likes_count,
                                                         'like_user': like_user,
                                                         'like_usr': like_usr,
                                                         'user_f': user_f,
                                                         'fav': fav,
                                                         'fav_count': fav_count,
                                                         'fav_user': fav_user,
                                                         'fa_user': fa_user,
                                                          'base_post': base_post
                                                         })

    return render(request, 'myapp/postdetail.html', {'user': user,
                                                     'postdet': postdet,
                                                     'followers': followers,
                                                     'following': following,
                                                     'user_1': user_1,
                                                     'user_2': user_2,
                                                     'user_3': user_3,
                                                     'comments': comments,
                                                     'form': form,
                                                     'c': c,
                                                     'likes': likes,
                                                     'likes_count': likes_count,
                                                     'like_usr': like_usr,
                                                     'user_f': user_f,
                                                     'fav': fav,
                                                     'fav_count': fav_count,
                                                     'fav_user': fav_user,
                                                     'fa_user': fa_user,
                                                          'base_post': base_post
                                                     })



@login_required(login_url="/myapp/login/", redirect_field_name='')
def message_view(request, id):
    user_p = get_object_or_404(User_info, id=request.user.id)
    user_r = get_object_or_404(User_info, id=id)
    user_f = user_r.related_to.filter(from_user__rel_status=1).distinct()
    message = user_r.msg_sender.all()|user_r.msg_reciever.all().order_by('id')
    message_tim = user_r.msg_sender.all()|user_r.msg_reciever.filter(msg_reciever__username=user_r.username).order_by('-id')[:1]
    post_d = user_p.post_info_set.order_by('id')
    post_dt = Post_info.objects.all().distinct().order_by('-id')
    base_post = Post_info.objects.order_by('-id') [:10]

    if request.method == 'POST':
        if 'send_msg' in request.POST:
            send_message = Message.objects.get_or_create(
                msg_sender = user_p,
                msg_reciever = user_r,
                msg_content = request.POST.get('msg_content'),
                msg_publish_date = timezone.now(),
                msg_publish_time = datetime.datetime.now()
                )
            return render(request, 'myapp/messages.html', {'user_p': user_p,
                                                           'post_dt': post_dt,
                                                           'user_r': user_r,
                                                           'post_d': post_d,
                                                           'send_message': send_message,
                                                           'message': message,
                                                           'user_f': user_f,
                                                           'message_tim': message_tim,
                                                          'base_post': base_post
                                                           })
        return render(request, 'myapp/messages.html', {'user_p': user_p,
                                                       'post_dt': post_dt,
                                                       'user_r': user_r,
                                                       'post_d': post_d,
                                                       'message': message,
                                                       'user_f': user_f,
                                                       'message_tim': message_tim,
                                                          'base_post': base_post
                                                       })
    return render(request, 'myapp/messages.html', {'user_p': user_p,
                                                   'post_dt': post_dt,
                                                   'user_r': user_r,
                                                   'post_d': post_d,
                                                   'message': message,
                                                   'user_f': user_f,
                                                   'message_tim': message_tim,
                                                          'base_post': base_post
                                                   })


@login_required(login_url="/myapp/login/", redirect_field_name='')
def addpost_viw(request):
    user = get_object_or_404(User_info, id=request.user.id)
    add_post = Post_info.objects.all()
    base_post = Post_info.objects.order_by('-id') [:10]

    if request.method == 'POST':
        form = AddPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.post_user_id = request.user.id
            post.post_title = request.POST.get('post_title')
            post.post_desc = request.POST.get('post_desc')
            post.post_file = request.FILES.get('post_file')
            post.post_disp_img = request.FILES.get('post_disp_img')
            post.post_publish_date = timezone.now()
            post.post_publish_time = datetime.datetime.now()
            post.post_video_url = request.POST.get('post_video_url')
#            form.tags = request.POST.get('tags')
            post.save()
            form.save_m2m()
            return HttpResponseRedirect('/myapp/myprofile/')

        else:
            return HttpResponse('Invalid Details!!')
    else:
        form = AddPostForm()
        return render(request, 'myapp/addpost.html', {'form': form,
                                                      'add_post': add_post,
                                                      'user': user,
                                                          'base_post': base_post})


@login_required(login_url="/myapp/login/", redirect_field_name='')
def useredit_viw(request):
    user = get_object_or_404(User_info, id=request.user.id)
    userlist = User_info.objects.get(username=request.user.username)
    new_passwd = request.POST.get('password')
    rep_passwd = request.POST.get('rep_password')
    base_post = Post_info.objects.order_by('-id') [:10]

    if request.method == 'POST':
        if 'info_sav' in request.POST:
            form = UserInfoForm(data=request.POST, files=request.FILES,instance=request.user)
            if new_passwd == rep_passwd:
                if form.is_valid():
                    user.first_name = request.POST.get('first_name', user.first_name)
                    user.last_name = request.POST.get('last_name', user.last_name)
                    user.email = request.POST.get('email', user.email)
                    user.user_country = request.POST.get('user_country', user.user_country)
                    user.user_city = request.POST.get('user_city', user.user_city)
                    user.user_web_url = request.POST.get('user_web_url', user.user_web_url)
                    user.user_pic = request.FILES.get('user_pic', user.user_pic)
                    user.save()
                    return HttpResponseRedirect('/myapp/useredit/')
                else:
                    return HttpResponse('Invalid details!!')
            else:
                return HttpResponse('Passwords did not match!!!')
        if 'pass_sav' in request.POST:
            form = PasswordChangeForm(data=request.POST, instance=request.user)
            old_pass = request.POST.get('old_password')
            new_pass = request.POST.get('password')
            rep_pass = request.POST.get('rep_password')
            if form.is_valid():
                if user.check_password(old_pass):
                    if new_pass == rep_pass:
                        userlist.set_password(form.cleaned_data['password'])
                        userlist.save()
                        return HttpResponseRedirect('/myapp/useredit')
                    else:
                        return HttpResponse('Passwords does not match!!')
                else:
                    return HttpResponse('Invalid password!!')
            else:
                return HttpResponse('Invalid details!!')
        if 'abtme_sav' in request.POST:
            form = AboutMeInfoForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                user.user_abtme_title = request.POST.get('user_abtme_title')
                user.user_abtme_desc = request.POST.get('user_abtme_desc')
                user.save()
                return HttpResponseRedirect('/myapp/useredit')
            else:
                return HttpResponse('Invalid details!!')
    else:
        form = UserInfoForm()
        return render(request, 'myapp/useredit.html', {'user': user,
                                                       'form': form,
                                                          'base_post': base_post})


def user_authn(request):
    userlist = User_info.objects.all()
    base_post = Post_info.objects.order_by('-id') [:10]
    ret_message = 'Invalid Username or Password!!! Please try again.'
    rat_message2 = 'Invalid Email!!! Please try again.'
    sucess_msg = 'Account created sucessfully!!'
    login_form = LoginForm()
    reg_form = RegisterForm()

    if request.method == 'POST':
        if 'signin' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    user_ad = get_object_or_404(User_info, id=request.user.id)
                    user_p = get_object_or_404(User_info, id=request.user.id)
                    post_d = user_p.post_info_set.order_by('id')
                    get_post = Post_info.objects.order_by('-id')[:5]
                    post_dt = Post_info.objects.all().distinct().order_by('-id')
                    user_r = user_p.user_relationship.filter(to_user__rel_status=1)
                    user_s = user_p.user_relationship.filter(to_user__rel_status=3)
                    user_t = user_r | user_s
                    return render(request, 'myapp/index.html/', {'user': user,
                                                                 'user_ad': user_ad,
                                                                 'user_p': user_p,
                                                                 'post_dt': post_dt,
                                                                 'user_r': user_r,
                                                                 'post_d': post_d,
                                                                 'user_t': user_t,
                                                                 'get_post': get_post,
                                                          'base_post': base_post
                                                                 })
                else:
                    return render(request, 'myapp/login.html', {'ret_message': ret_message})
            else:
                return render(request, 'myapp/login.html', {'ret_message': ret_message})
        elif 'signup' in request.POST:
            if request.method == 'POST':
                form = RegisterForm(request.POST, request.FILES)
                if form.is_valid():
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password'])
                    user.save()
                    Relationship.objects.get_or_create(
                        rel_from_user=user,
                        rel_to_user=user,
                        rel_status=3
                    )
                    user.user_pic = ''
                    return render(request, 'myapp/login.html/', {'sucess_msg': sucess_msg})
                else:
                    return render(request, 'myapp/login.html', {'rat_message2': rat_message2})
    else:
        return render(request, "myapp/login.html", {'form': login_form,
                                                    'form': reg_form,
                                                    'userlist': userlist,
                                                          'base_post': base_post})


@login_required(login_url="/myapp/login/", redirect_field_name='')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/myapp/login/')



def forgot_password(request):
    if request.method == 'POST':
        usernm = request.POST.get('username')
        userfname = request.POST.get('firstname')
        userlname = request.POST.get('lastname')
        usereml = request.POST.get('email')
        usersecques = request.POST.get('secques')
        usersecans = request.POST.get('secans')
        old_pass = request.POST.get('reppass')
        new_pass = request.POST.get('password')
        userlist = User_info.objects.get(username=usernm)
        userfirstname = User_info.objects.get(first_name=userfname)
        userlastname = User_info.objects.get(last_name=userlname)
        useremail = User_info.objects.get(email=usereml)
        userques = User_info.objects.get(user_sec_ques=usersecques)
        userans = User_info.objects.get(user_sec_ans=usersecans)
        form = ForgotPassword(data=request.POST)
        base_post = Post_info.objects.order_by('id')[:10]

        if userlist != 0:
            if userfirstname != 0:
                if userlastname !=0:
                    if useremail !=0:
                        if userques !=0:
                            if userans !=0:
                                if old_pass == new_pass:
                                    if form.is_valid():
                                        userlist.set_password(form.cleaned_data['password'])
                                        userlist.save()
                                        return HttpResponseRedirect('/myapp/login/')
                                    else:
                                        return render(request, 'myapp/login.html', {})
                                else:
                                    HttpResponse('Passwords do not match')
                            else:
                                HttpResponse('Invalid details')
                        else:
                            HttpResponse('Invalid details')
                    else:
                        HttpResponse('Invalid details')
                else:
                    HttpResponse('Invalid details')
            else:
                HttpResponse('Invalid details')
        else:
            HttpResponse('Invalid details')
    else:
        form = ForgotPassword()
        return render(request, "myapp/forgot-password.html", {'form': form})















