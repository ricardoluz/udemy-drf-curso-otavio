from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from ..models import Recipe
from tag.models import Tag

from ..serializers import RecipeSerializer, TagSerializer

from ..permissions import IsOwner
from django.shortcuts import get_object_or_404


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 1


class RecipeApiv2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination
    http_method_names = ["get", "options", "head", "patch", "delete"]

    # Permite a apenas leitura quando não estiver autenticado.
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Sobrescrevendo o método create para guardar o author.
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # Linha alterada.
        # TODO: Retirar o [is_published=True] do save.
        serializer.save(author=request.user, is_published=True)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    # ALterar o permissionamento para realizar alterações.
    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsOwner()]

        return super().get_permissions()

    # Sobrescrever o método de obtenção do objeto.
    # De forma a validar as permissões de uso do objeto
    # quando ele for chamado.
    def get_object(self):
        pk = self.kwargs.get("pk")
        obj = pk = get_object_or_404(
            self.get_queryset(),
            pk=pk,
        )

        self.check_object_permissions(self.request, obj)
        return obj

    # Sobrecreve

    # Exemplo de personalização de um método que está embutido na  ...APIView
    # Sendo sobrescrito.
    def partial_update(self, request, *args, **kwargs):
        # pk = kwargs.get("pk")
        # recipe = self.get_queryset().filter(pk=pk).first()
        recipe = self.get_object()
        serializer = RecipeSerializer(
            instance=recipe,
            many=False,
            context={"request": request},
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            # TODO: temporário para criar os dados de ...
            # author_id=1,
            # category_id=1,
            # tags=[1, 2],
        )
        return Response(serializer.data)


@api_view()
def tag_api_detail(request, pk):

    tag = Tag.objects.filter(pk=pk).first()

    if tag:
        serializer = TagSerializer(
            instance=tag,
            many=False,
            # context={"request": request},
        )
        return Response(serializer.data)
    else:
        return Response(
            status=status.HTTP_404_NOT_FOUND,
            data={
                "detail": "Registro inexistente",
            },
        )
