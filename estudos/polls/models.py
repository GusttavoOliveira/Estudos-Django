from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self) -> str:
        return self.question_text
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now()


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.choice_text

# Aqui, cada modelo é representado por uma classe derivada da classe django.db.models.Model. 
# Cada modelo possui alguns atributos de classe, as quais por sua vez representa um campo do banco de dados no modelo.

# Cada campo é representado por uma instância de uma classe Field
# por exemplo, CharField para campos do tipo caractere e DateTimeField para data/hora. 
# Isto diz ao Django qual tipo de dado cada campo contém