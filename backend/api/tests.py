from unittest.mock import Mock

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from .views import UserViewSet

User = get_user_model()


class TestUserDeactivateView(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@mail.ru',
            password='testpass123'
        )

    def create_authenticated_request(self, method, path, user=None):
        """Вспомогательный метод для создания аутентифицированного request"""
        if method.upper() == 'DELETE':
            wsgi_request = self.factory.delete(path)
        elif method.upper() == 'GET':
            wsgi_request = self.factory.get(path)
        elif method.upper() == 'POST':
            wsgi_request = self.factory.post(path)
        elif method.upper() == 'PUT':
            wsgi_request = self.factory.put(path)
        else:
            raise ValueError(f"Unsupported method: {method}")

        request = Request(wsgi_request)
        request.user = user

        return request

    def test_deactivate_permission_unauthorized(self):
        """
        Тест: неавторизованный пользователь не может деактивировать аккаунт
        """
        mock_view = Mock(spec=UserViewSet)
        mock_view.action = 'delete'

        request = self.factory.delete('/api/users/me/')

        request.user = None

        permission = IsAuthenticated()
        result = permission.has_permission(request, mock_view)

        self.assertFalse(result)

    def test_deactivate_permission_authorized(self):
        """
        Тест: авторизованный пользователь может деактивировать аккаунт
        """
        mock_view = Mock(spec=UserViewSet)
        mock_view.action = 'destroy'

        request = self.create_authenticated_request(
            'DELETE',
            '/api/users/me/',
            user=None
            )

        permission = IsAuthenticated()
        result = permission.has_permission(request, mock_view)

        self.assertFalse(result)
