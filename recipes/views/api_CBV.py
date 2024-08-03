from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.shortcuts import get_object_or_404

from ..models import Recipe
from tag.models import Tag

from ..serializers import RecipeSerializer, TagSerializer


class RecipeAPIv2List(APIView):
    def get(self, request):
        recipes = Recipe.objects.get_published()[:10]
        serializer = RecipeSerializer(
            instance=recipes,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = RecipeSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            # TODO: temporário para criar os dados de ...
            # author_id=1,
            # category_id=1,
            # tags=[1, 2],
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RecipeAPIv2Detail(APIView):
    def get_recipe(self, pk):

        recipe = get_object_or_404(Recipe.objects.get_published(), pk=pk)
        return recipe

    def get(self, request, pk):
        serializer = RecipeSerializer(
            instance=self.get_recipe(pk),
            many=False,
            context={"request": request},
        )
        return Response(serializer.data)

    def patch(self, request, pk):
        serializer = RecipeSerializer(
            instance=self.get_recipe(pk),
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

    def delete(self, request, pk):
        recipe = self.get_recipe(pk)
        recipe.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
            data={
                "detail": "Registro excluído",
            },
        )


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
