from django.contrib.auth import logout
from djoser.views import Response
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


class UserViewSet(DjoserUserViewSet):
    def get_permissions(self):
        """
        Переопределяем permissions:
        - Для эндпоинта 'me' - только аутентифицированные пользователи
        - Для остальных действий (retrieve, list) - разрешаем всем
        """
        if self.action == 'me':
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        """
        Переопределяем DELETE /users/me/ для мягкого удаления
        """
        user = request.user

        # Мягкое удаление - просто деактивируем
        user.is_active = False
        user.save()

        # Удаляем все токены
        Token.objects.filter(user=user).delete()

        # Выход из текущей сессии
        logout(request)

        return Response(
            {"detail": "Аккаунт успешно деактивирован"},
            status=status.HTTP_204_NO_CONTENT
        )
