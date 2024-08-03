from collections import defaultdict

from django.core.exceptions import ValidationError
from utils.strings import is_positive_number


class AuthorRecipeValidator:
    def __init__(self, data, errors=None, ErrorClass=None):

        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.clean()  # Chamar o processo de validação ao instanciar a classe.

    def clean(self, *args, **kwargs):
        # Chamar os outros métodos de validação
        self.clean_title()
        self.clean_servings()
        self.clean_preparation_time()

        # super_clean = super().clean(*args, **kwargs)
        cd = self.data

        title = cd.get("title")
        description = cd.get("description")

        if title == description:
            self.errors["title"].append("Cannot be equal to description")
            self.errors["description"].append("Cannot be equal to title")

        if self.errors:
            raise self.ErrorClass(self.errors)

        # return super_clean

    def clean_title(self):
        title = self.data.get("title")

        if len(title) < 5:
            self.errors["title"].append("Must have at least 5 chars.")

        return title

    def clean_preparation_time(self):
        field_name = "preparation_time"
        field_value = self.data.get(field_name)

        if not is_positive_number(field_value):
            self.errors[field_name].append("Must be a positive number")

        return field_value

    def clean_servings(self):
        field_name = "servings"
        field_value = self.data.get(field_name)

        if not is_positive_number(field_value):
            self.errors[field_name].append("Must be a positive number")

        return field_value
