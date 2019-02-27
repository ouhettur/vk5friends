from django.shortcuts import render
from .vkapi import VkUser
from allauth.socialaccount.models import SocialAccount


def index(request):
    user = request.user
    data = {'is_authenticated': user.is_authenticated}
    if not data['is_authenticated']:
        return render(request, 'app/baseapp.html', {'data': data})
    data['username'] = user.first_name + ' ' + user.last_name
    social_account = SocialAccount.objects.get(user=request.user)
    data['photo'] = social_account.extra_data['photo_max_orig']
    data['user_vk_id'] = social_account.uid
    vk_user = VkUser(user)
    data['friends_data'] = vk_user.get_friends(count=5)
    if data['friends_data']['available_status'] == 'not_enough_permissions':
        return render(request, 'app/permission_error.html', {'data': data}, status=422)
    elif data['friends_data']['available_status'] != 'available':
        return render(request, 'app/base_error.html', {'data': data}, status=422)
    return render(request, 'app/5friend.html', {'data': data})
