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
