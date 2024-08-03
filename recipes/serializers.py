from rest_framework import serializers

# from django.contrib.auth.models import User

from recipes.models import Recipe
from tag.models import Tag

from authors.validator import AuthorRecipeValidator


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "description",
            "public",
            "preparation",
            "preparation_time",
            "preparation_time_unit",
            "servings",
            "servings_unit",
            "preparation_steps",
            "cover",
            "author",
            "author_name",
            "author_id",
            "category",
            "category_name",
            "tags",
            "tag_links",
            "tag_objects",
            "tag_links",
            "slug_",
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

    slug_ = serializers.SlugField(source="slug", read_only=True)

    def get_preparation(self, recipe):
        return f"{recipe.preparation_time} {recipe.preparation_time_unit}"

    def validate(self, attrs):
        # Adaptação para ler os campos e realizar um PATCH.
        if self.instance is not None:
            if attrs.get("servings") is None:
                attrs["servings"] = self.instance.servings
            if attrs.get("preparation_time") is None:
                attrs["preparation_time"] = self.instance.servings

        super_validate = super().validate(attrs)
        AuthorRecipeValidator(
            data=attrs,
            ErrorClass=serializers.ValidationError,
        )
        return super_validate

    def save(self, **kwargs):
        # Modificação do save para receber parâmetros adicionais.
        return super().save(**kwargs)
