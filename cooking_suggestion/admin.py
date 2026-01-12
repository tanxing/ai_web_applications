from django.contrib import admin
from django.db import models

# from django_json_widget.widgets import JSONEditorWidget
from .models import Recipe


# Register your models here.
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "ingredient1",
        "ingredient2",
        "ingredient3",
        "ingredient4",
        "ingredient5",
        "instructions",
    )


#   formfield_overrides = {
#     models.JSONField: {'widget': JSONEditorWidget},
#   }
admin.site.register(Recipe, RecipeAdmin)
