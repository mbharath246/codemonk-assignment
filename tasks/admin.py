from django.contrib import admin
from tasks import models

admin.site.register(models.Paragraph)
admin.site.register(models.TokenizedWords)
