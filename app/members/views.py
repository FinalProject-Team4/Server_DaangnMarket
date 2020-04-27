from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from members.models import SelectedLocation
from members.serializers import (
    IdTokenSerializer,
    UserSerializer,
    SignUpSerializer,
    SetLocateSerializer
)
from members.swaggers import decorated_login_api, decorated_signup_api, decorated_set_locate_create_edit_api, \
    decorated_set_locate_delete_api, decorated_set_locate_list_api

User = get_user_model()


def entry_view(request):
    return render(request, "members/sign_in_with_phone.html")


def signup_view(request):
    return render(request, "members/sign_up.html")


@method_decorator(name='post', decorator=decorated_login_api)
class LoginAPI(GenericAPIView):
    """
    로그인

    ### POST _/members/login/_
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

    ### POST _/members/signup/_
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


class UserInfoAPI(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        return super(UserInfoAPI, self).retrieve(request, *args, **kwargs);

    def partial_update(self, request, *args, **kwargs):
        return super(UserInfoAPI, self).partial_update(request, *args, **kwargs);

    def destroy(self, request, *args, **kwargs):
        return super(UserInfoAPI, self).destroy(request, *args, **kwargs);

    def get_object(self):
        user = self.request.user
        return user


class SetLocateAPI(ModelViewSet):
    queryset = SelectedLocation.objects.all()
    serializer_class = SetLocateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    @method_decorator(decorator=decorated_set_locate_list_api)
    def list(self, request, *args, **kwargs):
        """
        내 동네 설정 목록

        ### GET _/members/locate/_
        """
        return super(SetLocateAPI, self).list(request, *args, **kwargs)

    @method_decorator(decorator=decorated_set_locate_create_edit_api)
    def create(self, request, *args, **kwargs):
        """
        내 동네 설정 저장

        ### POST _/members/locate/_
        """
        return super(SetLocateAPI, self).create(request, *args, **kwargs)

    @method_decorator(decorator=decorated_set_locate_create_edit_api)
    def partial_update(self, request, *args, **kwargs):
        """
        내 동네 설정 수정

        ### PATCH _/members/locate/_
        """
        return super(SetLocateAPI, self).partial_update(request, *args, **kwargs)

    @method_decorator(decorator=decorated_set_locate_delete_api)
    def destroy(self, request, *args, **kwargs):
        """
        내 동네 설정 삭제

        ### DELETE _/members/locate/_
        """
        return super(SetLocateAPI, self).destroy(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        ret = user.user_selected_locations
        return ret

    def get_object(self):
        locate = self.request.data['locate']
        qs = self.get_queryset()
        ret = qs.filter(locate_id=locate).get()
        return ret
