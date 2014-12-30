#!/usr/bin/env python
import oauth2 as oauth
import time
import md5
import hashlib
import hmac
import base64
import urllib
import cgi
import json

class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Other than that, there are
    no restrictions that apply to the decorated class.

    To get the singleton instance, use the `Instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    Limitations: The decorated class cannot be inherited from.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def Instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)

@Singleton
class Oauth:
    def __init__(self):
        self.request_token_url = "https://www.snucse.org/app/RequestToken"
        self.access_token_url = "https://www.snucse.org/app/AccessToken"
        self.authorize_url = "https://www.snucse.org/app/Authorize"
        self.user_bs_class_year_url = "https://www.snucse.org/app/1/user/bsclassyear.json"
        self.oauth_consumer_secret = '6925671658e1e7369d532b-2b69-40fe-aa5e-68863a224882'
        self.oauth_consumer_key = '410172'
        self.oauth_callback = 'http://dew.snucse.org:9999'
        self.oauth_signature_method = 'HMAC-SHA1'
        self.oauth_version = '1.0'
        self.consumer = oauth.Consumer(self.oauth_consumer_key, self.oauth_consumer_secret)

    def get_request_token(self):
        oauth_timestamp = str(int(time.time()))
        oauth_nonce = md5.md5(oauth_timestamp).hexdigest()
        params = {}
        params['oauth_consumer_key'] = urllib.quote_plus(self.oauth_consumer_key)
        params['oauth_callback'] = urllib.quote_plus(self.oauth_callback)
        params['oauth_signature_method'] = urllib.quote_plus(self.oauth_signature_method)
        params['oauth_timestamp'] = urllib.quote_plus(oauth_timestamp)
        params['oauth_nonce'] = urllib.quote_plus(oauth_nonce)
        params['oauth_version'] = urllib.quote_plus(self.oauth_version)
        sig_base = "GET&{0}&{1}".format(urllib.quote_plus(self.request_token_url), urllib.urlencode(sorted(params.items())))
        sig_key = "{0}&".format(self.oauth_consumer_secret)
        oauth_signature = base64.b64encode(hmac.new(sig_key, sig_base, hashlib.sha1).digest())
        params = urllib.urlencode({
            'oauth_consumer_key' : self.oauth_consumer_key,
            'oauth_callback' : self.oauth_callback,
            'oauth_signature_method' : self.oauth_signature_method,
            'oauth_timestamp' : oauth_timestamp,
            'oauth_nonce' : oauth_nonce,
            'oauth_version' : self.oauth_version,
            'oauth_signature' : oauth_signature
            })
        client = oauth.Client(self.consumer)
        response, content = client.request(self.request_token_url, 'POST', params)
        print("Requested : {0}".format(self.request_token_url))
        print("Response : {0}".format(response))
        print("Content : {0}".format(content))
        parsed_content = dict(cgi.parse_qsl(content))
        oauth_token = parsed_content['oauth_token']
        oauth_token_secret = parsed_content['oauth_token_secret']
        request_token = oauth.Token(oauth_token, oauth_token_secret)
        return request_token

    def get_authorize_url(self, request_token):
        if request_token is None:
            return None
        return "{0}?oauth_token={1}".format(self.authorize_url, request_token.key)

    def get_access_token(self, request_token, oauth_verifier):
        if request_token is None:
            return None
        elif oauth_verifier is None:
            return None
        request_token.set_verifier(oauth_verifier)
        client = oauth.Client(self.consumer, request_token)
        response, content = client.request(self.access_token_url, 'POST')
        print("Requested : {0}".format(self.access_token_url))
        print("Response : {0}".format(response))
        print("Content : {0}".format(content))
        parsed_content = dict(cgi.parse_qsl(content))
        oauth_token = parsed_content['oauth_token']
        oauth_token_secret = parsed_content['oauth_token_secret']
        access_token = oauth.Token(oauth_token, oauth_token_secret)
        return access_token

    def get_bs_class_year(self, access_token):
        if access_token is None:
            return None, None, None
        client = oauth.Client(self.consumer, access_token)
        response, content = client.request(self.user_bs_class_year_url, 'POST')
        print("Requested : {0}".format(self.user_bs_class_year_url))
        print("Response : {0}".format(response))
        print("Content : {0}".format(content))
        data = json.loads(content)
        return data.get("Name"), data.get("Account"), data.get("BsYear")
