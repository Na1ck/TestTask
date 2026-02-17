from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class MockProjectView(APIView):
    """
    Mock-View для работы с проектами
    Демонстрирует: GET (список), POST (создание), мягкое удаление
    """
    permission_classes = [IsAuthenticated]

    mock_projects = [
        {
            'id': 1,
            'name': 'Разработка мобильного приложения',
            'description': 'Создание iOS и Android версий',
            'status': 'active',
            'owner_id': 1,
            'created_at': '2026-01-15T10:00:00Z',
            'team_size': 5
        },
        {
            'id': 2,
            'name': 'Редизайн сайта',
            'description': 'Обновление UI/UX корпоративного сайта',
            'status': 'active',
            'owner_id': 1,
            'created_at': '2026-02-01T14:30:00Z',
            'team_size': 3
        },
        {
            'id': 3,
            'name': 'Интеграция с платежной системой',
            'description': 'Подключение нового платежного шлюза',
            'status': 'archived',
            'owner_id': 2,
            'created_at': '2025-12-10T09:15:00Z',
            'archived_at': '2026-01-20T16:45:00Z',
            'team_size': 2
        }
    ]

    def get(self, request):
        """GET /api/mock/projects/ - список проектов"""
        return Response(self.mock_projects)

    def post(self, request):
        """POST /api/mock/projects/ - создать проект"""
        # Простая валидация
        if 'name' not in request.data:
            return Response(
                {'error': 'Поле name обязательно'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Создаем новый проект
        new_project = {
            'id': len(self.mock_projects) + 1,
            'name': request.data.get('name'),
            'description': request.data.get('description', ''),
            'status': 'active',
            'owner_id': request.user.id,
            'created_at': '2026-02-17T12:00:00Z',
            'team_size': 1
        }

        return Response(new_project, status=status.HTTP_201_CREATED)


class MockProjectDetailView(APIView):
    """
    Mock-View для детальной работы с проектом
    Демонстрирует: GET (детали), PUT (обновление), DELETE (мягкое удаление)
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, project_id):
        """Получить проект по ID (мок)"""
        mock_projects = {
            1: {
                'id': 1,
                'name': 'Разработка мобильного приложения',
                'description': 'Создание iOS и Android версий',
                'status': 'active',
                'owner_id': 1,
                'created_at': '2026-01-15T10:00:00Z',
                'tasks_count': 12,
                'completed_tasks': 5
            },
            2: {
                'id': 2,
                'name': 'Редизайн сайта',
                'description': 'Обновление UI/UX',
                'status': 'active',
                'owner_id': 1,
                'created_at': '2026-02-01T14:30:00Z',
                'tasks_count': 8,
                'completed_tasks': 2
            }
        }

        project = mock_projects.get(project_id)
        if not project:
            raise Http404("Проект не найден")

        # Проверка прав доступа (только владелец или админ)
        if project['owner_id'] != (self.request.user.id
                                   and not self.request.user.is_staff):
            return None, "Нет прав доступа к этому проекту"

        return project, None

    def get(self, request, pk):
        """GET /api/mock/projects/{pk}/ - детали проекта"""
        project, error = self.get_object(pk)

        if error:
            return Response(
                {'error': error},
                status=status.HTTP_403_FORBIDDEN)

        if not project:
            return Response(
                {'error': 'Проект не найден'},
                status=status.HTTP_404_NOT_FOUND)

        return Response(project)

    def put(self, request, pk):
        """PUT /api/mock/projects/{pk}/ - обновить проект"""
        project, error = self.get_object(pk)

        if error:
            return Response(
                {'error': error},
                status=status.HTTP_403_FORBIDDEN)

        if not project:
            return Response(
                {'error': 'Проект не найден'},
                status=status.HTTP_404_NOT_FOUND)

        # Обновляем поля
        if 'name' in request.data:
            project['name'] = request.data['name']
        if 'description' in request.data:
            project['description'] = request.data['description']

        return Response({
            'message': 'Проект обновлен',
            'project': project
        })

    def delete(self, request, pk):
        """DELETE /api/mock/projects/{pk}/ - мягкое удаление проекта"""
        project, error = self.get_object(pk)

        if error:
            return Response(
                {'error': error},
                status=status.HTTP_403_FORBIDDEN)

        if not project:
            return Response(
                {'error': 'Проект не найден'},
                status=status.HTTP_404_NOT_FOUND)

        project['status'] = 'archived'
        project['archived_at'] = '2026-02-17T14:30:00Z'

        return Response(
            {'message': 'Проект архивирован'},
            status=status.HTTP_204_NO_CONTENT
        )
