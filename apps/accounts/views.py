from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    AuthResponseSerializer,
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)


@extend_schema(tags=["auth"], request=RegisterSerializer, responses={201: AuthResponseSerializer})
class RegisterView(generics.GenericAPIView):
    """Регистрация. Сразу возвращает токены, повторно входить не нужно."""

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": UserSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(tags=["auth"], responses={200: AuthResponseSerializer})
class LoginView(TokenObtainPairView):
    """Вход по email и паролю."""

    serializer_class = LoginSerializer


from drf_spectacular.utils import extend_schema  # noqa: E402
from rest_framework.permissions import IsAuthenticated  # noqa: E402
from rest_framework.response import Response  # noqa: E402
from rest_framework.views import APIView  # noqa: E402

from .serializers import UserSerializer  # noqa: E402


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=UserSerializer)
    def get(self, request):
        """Данные текущего пользователя."""
        return Response(UserSerializer(request.user).data)
