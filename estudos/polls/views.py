from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from .models import Question, Choice
""
# Create your views here.

"""
Nós estamos usando duas views genéricas aqui: ListView e DetailView. Respectivamente, essas duas views abstraem o conceito 
de exibir uma lista de objetos e exibir uma página de detalhe para um tipo particular de objeto.

Cada “view” genérica precisa saber qual é o modelo que ela vai agir. Isto é fornecido usando o atributo model.
A view genérica DetailView espera o valor de chave primaria capturado da URL chamada "pk", então mudamos question_id para pk para as views genérica.
"""

"""
Nas partes anteriores deste tutorial, os templates tem sido fornecidos com um contexto que contém as variáveis question e latest_question_list. Para a DetailView a variavel question é fornecida automaticamente – já que estamos usando um modelo Django (Question), Django é capaz de determinar um nome apropriado para a variável de contexto. Contudo, para ListView, a variável de contexto gerada automaticamente é question_list. Para sobrescrever nós fornecemos o atributo context_object_name, especificando que queremos usar latest_question_list no lugar.
"""

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self) -> QuerySet[Any]:
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    # Usando o método POST[] da variável request eu posso me referir aos dados que forem submetidos na página.
    # (<input type="submit">)   Eu posso manipular esses dados em forma de dicionário.
    # Neste caso, request.POST['choice'] retorna o ID da opção selecionada, como uma string. 
    # Os valores de request.POST são sempre strings.
    try:
        # Vai na request, acessa a o valor do <input> cujo atributo name é 'choice'
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Reexibe o formulario de voto da pergunta
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Você não selecionou uma opção."
            })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Sempre retonra um HttpResponseRedirect depois que o POST for bem sucedido.
        # Isso previne que os dados sejam postados duas vezes se o usuário apertar o
        # botão de voltar.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
