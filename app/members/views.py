import os

import firebase_admin
from django.contrib.auth import get_user_model
from django.shortcuts import render
from firebase_admin import auth, credentials
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from members.serializers import UserSerializer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)

cred = credentials.Certificate(f"{ROOT_DIR}/serviceAccountKey.json")
default_app = firebase_admin.initialize_app(cred)

User = get_user_model()


def entry_view(request):
    return render(request, "sign_in_with_phone.html")


def signup_view(request):
    return render(request, "sign_up.html")


class Entry(APIView):
    def post(self, request):
        id_token = request.data.get('idToken', None)
        username = request.data.get('username', None)

        if not id_token:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif not username:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        decoded_token = auth.verify_id_token(id_token)
        phone = decoded_token['phone_number']
        uid = decoded_token['uid']

        user, created = User.objects.get_or_create(uid=uid, username=username)
        if not created:
            user.username = username
            user.phone = phone
            user.save()

        token, _ = Token.objects.get_or_create(user=user)

        data = {
            'Authorization': f'Token {token.key}',
            'User': UserSerializer(user).data,
        }

        print("user, created : ", user, created)
        print("token :", token)
        print("data :", data)

        return Response(data, status=status.HTTP_200_OK)
