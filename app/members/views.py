from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from members.models import SelectedLocation
from members.serializers import (
    IdTokenSerializer,
    UserSerializer,
    SignUpSerializer,
    SetLocateSerializer
)
from members.swaggers import decorated_login_api, decorated_signup_api, decorated_setlocate_api

User = get_user_model()


def entry_view(request):
    return render(request, "sign_in_with_phone.html")


def signup_view(request):
    return render(request, "sign_up.html")


@method_decorator(name='post', decorator=decorated_login_api)
class LoginAPI(GenericAPIView):
    """
    로그인

    ### _POST_ /members/login/
    """
    queryset = User.objects.all()
    serializer_class = IdTokenSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        # exceptions
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        try:
            user = authenticate(request, auth=serializer.data)
        except AuthenticationFailed:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(UserSerializer(user).data, status.HTTP_200_OK)


@method_decorator(name='post', decorator=decorated_signup_api)
class SignUpAPI(GenericAPIView):
    """
    회원 가입

    ### _POST_ /members/signup/
    """
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        # exceptions
        try:
            user = authenticate(auth=serializer.data)
            token, _ = Token.objects.get_or_create(user=user)
        except AuthenticationFailed:  # exceptions 다른거
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(UserSerializer(user).data, status.HTTP_200_OK)


@method_decorator(name='post', decorator=decorated_setlocate_api)
class SetLocateAPI(CreateAPIView):
    """
    내 동네 설정

    ### _POST_ /members/locate/
    """
    queryset = SelectedLocation.objects.all()
    serializer_class = SetLocateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        serializer = super(SetLocateAPI, self).get_serializer(*args, **kwargs)
        serializer.initial_data['user'] = self.request.user.pk
        return serializer
