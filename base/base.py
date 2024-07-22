from django.db import models

class BaseModel(models.Model):
    atividade = models.CharField(max_length=200)
    dataAtividade = models.DateField()
    local = models.CharField(max_length=200)
    horario = models.TimeField(default="00:00")
    descricao = models.TextField()

    class Meta:
        abstract = True