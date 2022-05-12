import api.models as models
from django.contrib import admin

LIST_MODELS = [
    models.User,
    models.Post,
    models.Blog,
    models.Read,
    models.Date
]

admin.site.register(LIST_MODELS)
