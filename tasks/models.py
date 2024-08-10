from django.db import models
from users.models import CustomUser


class Paragraph(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=50, unique=True, null=False)
    paragraphs = models.TextField()

    def __str__(self) -> str:
        return f'{self.uuid} user =  {self.user}'


class TokenizedWords(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    uuid = models.ForeignKey(Paragraph, on_delete=models.CASCADE)
    words = models.CharField(max_length=50)
    indexes = models.IntegerField()

    def __str__(self) -> str:
        return str(self.uuid)