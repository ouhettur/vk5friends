from allauth.socialaccount.models import SocialToken
import requests


class VkUser:
    def __init__(self, user):
        self.user_token = SocialToken.objects.filter(account__user=user, account__provider='vk')

    def get_friends(self, count=5) -> dict:
        args = {
            'v': 5.92,
            'fields': 'nickname, photo_200_orig',
            'count': count,
            'order': 'random',
            'access_token': self.user_token
        }
        friends_data = {'available_status': 'available'}
        try:
            response = requests.get('https://api.vk.com/method/friends.get', args)
        except requests.exceptions.RequestException:
            friends_data['available_status'] = 'request_error'
            return friends_data
        try:
            friends_data['friend_list'] = response.json()['response']['items']
        except KeyError:
            friends_data['available_status'] = VkUser.error_handler(response.json())
        return friends_data

    @staticmethod
    def error_handler(response: dict) -> str:
        if response['error']['error_code'] == 5:
            return 'not_enough_permissions'
        else:
            return 'uncaught error'
