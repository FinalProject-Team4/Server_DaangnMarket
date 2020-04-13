from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from members.serializers import *


User = get_user_model()


def entry_view(request):
    return render(request, "sign_in_with_phone.html")


def signup_view(request):
    return render(request, "sign_up.html")


class FirebaseLogin(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self, request):
        id_token = request.data.get('idToken', None)

        if not id_token:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            user = User.objects.get_or_none(uid=uid)
            if not user:
                raise ValueError
        except ValueError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class SignUp(APIView):
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    def post(self, request):

        try:
            id_token = request.data.get('idToken', None)
            decoded_token = auth.verify_id_token(id_token)
        except ValueError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        uid = decoded_token['uid']
        user_data = {
            'phone': decoded_token['phone_number'],
            'username': request.data.get('username', None),
            'avatar': request.data.get('avatar', None)
        }

        user, created = User.objects.update_or_create(defaults=user_data, uid=uid)

        token, _ = Token.objects.get_or_create(user=user)

        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
