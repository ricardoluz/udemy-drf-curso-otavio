from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from ..serializers import AuthorSerializer


class AuthorViewSet(ModelViewSet):

    serializer_class = AuthorSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]
    # Permitir obter, alterar e deletar o próprio dado.
    # Com a trava realizada no queryset (username = ...)
    http_method_names = ["get", "patch", "delete"]

    def get_queryset(self):
        User = get_user_model()
        qs = User.objects.filter(username=self.request.user.username)

        return qs

    @action(
        methods=["get"],
        detail=False,
    )  # Transforma o método para ser visto na view.
    def me(self, request, *args, **kwargs):
        obj = self.get_queryset().first()
        serializer = self.get_serializer(instance=obj)

        return Response(serializer.data)
