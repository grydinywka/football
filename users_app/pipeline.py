import urllib
from urlparse import urlparse
from django.core.files import File
import requests

from users_app.models import AvatarProfile


def get_avatar(backend, strategy, details, response, user=None, *args, **kwargs):
    url = None
    print backend.name
    if backend.name == 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large"%response['id']
    if backend.name == 'vk-oauth2':
        r = requests.get('https://api.vk.com/method/users.get?user_ids={}&fields=photo_100'.format(response['id']))
        if r.ok:
            url = r.json()['response'][0]['photo_100']

    if url:
        ava_profile, created = AvatarProfile.objects.get_or_create(user=user)
        if created:
            name = urlparse(url).path.split('/')[-1] + response['id'].__str__() + '.bmp'
            content = urllib.urlretrieve(url)

            # See also: http://docs.djangoproject.com/en/dev/ref/files/file/
            ava_profile.avatar.save(name, File(open(content[0])), save=True)
