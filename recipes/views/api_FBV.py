from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# from django.shortcuts import get_object_or_404

from ..models import Recipe
from tag.models import Tag

from ..serializers import RecipeSerializer, TagSerializer


@api_view(http_method_names=["GET", "POST"])
def recipe_api_list(request):
    if request.method == "GET":
        recipes = Recipe.objects.get_published()[:10]
        serializer = RecipeSerializer(
            instance=recipes,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)
    elif request.method == "POST":
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


@api_view(http_method_names=["GET", "PATCH", "DELETE"])
def recipe_api_detail(request, pk):
    # recipe = get_object_or_404(Recipe.objects.get_published(), pk=pk)
    # TODO: Estudar o método get_object_or_404(

    recipe = Recipe.objects.get_published().filter(pk=pk).first()

    if not recipe:
        return Response(
            status=status.HTTP_404_NOT_FOUND,
            data={
                "detail": "Registro inexistente",
            },
        )

    match request.method:
        case "GET":
            serializer = RecipeSerializer(
                instance=recipe,
                many=False,
                context={"request": request},
            )
            return Response(serializer.data)

        case "PATCH":
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

        case "DELETE":
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
