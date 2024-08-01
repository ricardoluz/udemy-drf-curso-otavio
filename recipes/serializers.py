from rest_framework import serializers
from django.contrib.auth.models import User

from recipes.models import Recipe, Category
from tag.models import Tag


class TagSerializer_old(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    slug = serializers.SlugField()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class RecipeSerializer_old(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=65)
    description = serializers.CharField(max_length=165)
    # renomeando um campo
    public = serializers.BooleanField(source="is_published")
    # Campo criado
    preparation = serializers.SerializerMethodField()
    # Campo relacionado
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
    )
    category_name = serializers.StringRelatedField(source="category")
    author = serializers.StringRelatedField()
    author_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )

    tag_objects = TagSerializer(source="tags", many=True)

    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source="tags",
        queryset=Tag.objects.all(),
        view_name="recipes:recipes_api_v2_tag",
    )

    def get_preparation(self, recipe):
        return f"{recipe.preparation_time} {recipe.preparation_time_unit}"


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "description",
            "public",
            "preparation",
            "author",
            "author_name",
            "author_id",
            "category",
            "category_name",
            "tags",
            "tag_links",
            "tag_objects",
            "tag_links",
        ]

    # renomeando um campo
    public = serializers.BooleanField(
        source="is_published",
        read_only=True,
    )
    # Campo criado
    preparation = serializers.SerializerMethodField()
    # Campo relacionado
    # category = serializers.PrimaryKeyRelatedField(
    #     queryset=Category.objects.all(),
    # )
    category_name = serializers.StringRelatedField(
        source="category",
        read_only=True,
    )
    author_name = serializers.StringRelatedField(
        source="author",
        read_only=True,
    )
    # author_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    tag_objects = TagSerializer(
        source="tags",
        many=True,
        read_only=True,
    )

    tag_links = serializers.HyperlinkedRelatedField(
        source="tags",
        many=True,
        view_name="recipes:recipes_api_v2_tag",
        read_only=True,
    )

    def get_preparation(self, recipe):
        return f"{recipe.preparation_time} {recipe.preparation_time_unit}"
