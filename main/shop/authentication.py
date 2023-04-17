from rest_framework import authentication


class BearerAuth(authentication.TokenAuthentication):
    keyword = 'Bearer'
