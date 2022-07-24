from django.contrib.auth.backends import ModelBackend, UserModel
from rest_framework.generics import get_object_or_404


class AuthenticationWithoutPassword(ModelBackend):

    def authenticate(self, request, username=None):
        if username is None:
            username = request.data.get('username', '')
        return get_object_or_404(UserModel, username=username)

    def get_user(self, user_id):
        return get_object_or_404(UserModel, pk=user_id)
