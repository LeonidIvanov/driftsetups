from urllib.request import urlopen

from social_core.backends.google import GoogleOAuth2
from social_core.backends.facebook import FacebookOAuth2
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist


def get_avatar(backend, user, response, *args, **kwargs):
    if not user.avatar:
        if isinstance(backend, GoogleOAuth2):
            if response.get('image') and response['image'].get('url'):
                url_sz50 = response['image'].get('url')
                url_no_sz = url_sz50.split('?')[0]
                url = '{}?sz=100'.format(url_no_sz)
                print(url)
        elif isinstance(backend, FacebookOAuth2):
            url = 'http://graph.facebook.com/{}/picture?width=100&height=100'.format(response['id'])
        try:
            ext = url.split('.')[-1]
            if '?' in ext:
                ext = ext.split('?')[0]
            user.avatar.save(
                '{0}.{1}'.format('avatar', ext),
                ContentFile(urlopen(url).read()),
                save=False
            )
            user.save()
        except ObjectDoesNotExist:
            print('Wrong backend provider!')
