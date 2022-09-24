from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from finder.postgresql_load import get_user_in_db, search_users
from .models import *
from finder.models import *

def login(request):
    return render(request, 'intro.html')


@login_required
def home(request):
    filter_enabled = True
    message = False

    user = User.objects.get(username=request.user)
    favorite_users = user.profile.favorite_users

    # TODO: fill info on auth
    social = request.user.social_auth.get(provider='vk-oauth2')

    token = social.extra_data['access_token']
    vk_id = int(social.uid)


    vk_db_user = get_user_in_db(vk_id, 'city_title, group_list, photo_200_orig')

    user.profile.vk_id = vk_id
    user.profile.vk_token = token
    user.profile.city_title = vk_db_user[0]
    user.profile.group_list = vk_db_user[1]
    user.profile.photo_200_orig = vk_db_user[2]
    user.save()


    if user.profile.city_title == '':
        message = 'Пожалуйста, укажите город в настройках профиля Вконтакте'
    elif favorite_users != [] and favorite_users != None:
        people = VkUsers.objects.filter(city_title='Пятигорск', is_closed=False).exclude(id__in=favorite_users)
    else:
        people = VkUsers.objects.filter(city_title='Пятигорск', is_closed=False)

    return render(request, 'home.html', {'filter_enabled': filter_enabled,
                                         'message': message,
                                         'people': people,
                                         'favorite': favorite})


@login_required
def profile(request):
    filter_enabled = False
    message = False

    user = User.objects.get(username=request.user.username)

    if user.profile.badges != [] and user.profile.badges != None:
        print(user.profile.badges)
        badges = Badge.objects.filter(code__in=user.profile.badges)

    else:
        badges = False

    return render(request, 'profile.html',
                            {'filter_enabled': filter_enabled,
                             'badges': badges,
                             'message':message})


@login_required
def favorite(request):
    filter_enabled = True
    user = User.objects.get(username=request.user)
    favorite_user_ids = user.profile.favorite_users

    favorite_users = VkUsers.objects.filter(id__in=favorite_user_ids)

    if favorite_users == None:
        favorite_users = False

    return render(request, 'favorite.html',
                            {'filter_enabled': filter_enabled,
                             'favorite_users': favorite_users})


@login_required
def favorite_add(request, user_id: int):
    filter_enabled = True
    user = User.objects.get(username=request.user)
    favorite_users = user.profile.favorite_users

    if request.POST:
        if user.profile.favorite_users != None:
            user.profile.favorite_users += [user_id]
            user.save()

        else:
            user.profile.favorite_users = [user_id]
            user.save()

    return redirect('/')


@login_required
def favorite_delete(request, user_id):
    filter_enabled = True
    user = User.objects.get(username=request.user)
    favorite_users = user.profile.favorite_users

    if request.POST:

        favorite_users.remove(user_id)
        user.save()

    return redirect('/favorite')


@login_required
def settings(request):
    filter_enabled = False
    user = User.objects.get(username=request.user)

    return render(request, 'settings.html', {'filter_enabled': filter_enabled})


@login_required
def enter_code(request):
    filter_enabled = False

    return render(request, 'enter_code.html', {'filter_enabled': filter_enabled})


def submit_code(request):
    filter_enabled = False

    if request.POST:
        try:
            badge = Badge.objects.get(code=request.POST['invite_code'])

            user = User.objects.get(username=request.user)

            if badge.code in user.profile.badges:
                message = "У вас уже есть этот значок!"

            else:
                user.profile.badges += [badge.code]
                user.save()

                print(f"{user.username} получает {badge.title}")

                message = f"Вы получаете  значок: {badge.title} "

            return render(request, 'enter_code.html',
                                   {'filter_enabled': filter_enabled,
                                    'message': message,
                                   })

        except Badge.DoesNotExist:
            message = 'Такого кода не существует!'
            return render(request, 'enter_code.html',
                                   {'filter_enabled': filter_enabled,
                                    'message':message,
                                   })
