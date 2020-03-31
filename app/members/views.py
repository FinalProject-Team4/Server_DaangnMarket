import os

import firebase_admin
from django.contrib.auth import get_user_model
from django.shortcuts import render
from firebase_admin import auth, credentials
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

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
        id_token = request.data['idToken']
        username = request.data['username']

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
            'token': token.key,
        }
        return Response(data)
