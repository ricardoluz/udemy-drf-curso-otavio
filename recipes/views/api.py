from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# from django.shortcuts import get_object_or_404

from ..models import Recipe
from tag.models import Tag

from ..serializers import RecipeSerializer, TagSerializer


@api_view(http_method_names=["get", "post"])
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
        serializer = RecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Post", status=status.HTTP_201_CREATED)


@api_view()
def recipe_api_detail(request, pk):
    # recipe = get_object_or_404(Recipe.objects.get_published(), pk=pk)
    # serializer = RecipeSerializer(instance=recipe, many=False)
    # return Response(serializer.data)

    recipe = Recipe.objects.get_published().filter(pk=pk).first()

    if recipe:
        serializer = RecipeSerializer(
            instance=recipe,
            many=False,
            context={"request": request},
        )
        return Response(serializer.data)
    else:
        return Response(
            status=status.HTTP_404_NOT_FOUND,
            data={
                "detail": "Registro inexistente",
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
