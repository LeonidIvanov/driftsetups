from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin


class WWWToNonWWWWRedirect(MiddlewareMixin):

    def process_request(self, request):
        hostname = request.get_host()
        if hostname[:4] == 'www.':
            abs_url = request.build_absolute_uri()
            abs_url = abs_url.replace('www.', '', 1)
            return HttpResponsePermanentRedirect(abs_url)


class AppendSlashRedirect(MiddlewareMixin):

    def process_request(self, request):
        abs_url = request.build_absolute_uri()
        if '?' in abs_url:
            uri, params = abs_url.split('?')
            if uri[-1] != '/':
                abs_url = '{0}/?{1}'.format(uri, params)
                return HttpResponsePermanentRedirect(abs_url)
        elif abs_url[-1] != '/' and 'robots.txt' not in abs_url:
            abs_url = '{}/'.format(abs_url)
            return HttpResponsePermanentRedirect(abs_url)
        # elif '.jpg' in abs_url or '.png' in abs_url or '.jpeg' in abs_url or '.bmp' in abs_url:
        #     pass


class EnToRuRedirect(MiddlewareMixin):

    def process_request(self, request):
        print(request.LANGUAGE_CODE)
        if request.LANGUAGE_CODE == 'ru':
            abs_url = request.get_full_path()
            return HttpResponsePermanentRedirect('https://driftsetups.com/ru{}'.format(abs_url))