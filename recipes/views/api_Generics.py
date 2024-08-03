from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.pagination import PageNumberPagination

from ..models import Recipe
from tag.models import Tag

from ..serializers import RecipeSerializer, TagSerializer


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 1


class RecipeAPIv2List(ListCreateAPIView):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination


class RecipeAPIv2Detail(RetrieveUpdateDestroyAPIView):

    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination

    # Exemplo de personalização de um método que está embutido na  ...APIView
    def partial_update(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        recipe = self.get_queryset().filter(pk=pk).first()
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
