from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Question, Choice
""
# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # Invoca o documento html criado em templates
    template = loader.get_template('polls/index.html')
    # Através do dicionário de contexto o html recebe as variáveis nele usadas
    context = {
        'latest_question_list': latest_question_list    
    }
    # Podemos gerar a resposta com HttpResponse(), usando a lib django.http
    # Ou pode-se usar a função render() passando os 3 parâmetros como a seguir:
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id) 
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    # Usando o método POST[] da variável request eu posso me referir aos dados que forem submetidos na página.
    # (<input type="submit">)   Eu posso manipular esses dados em forma de dicionário.
    # Neste caso, request.POST['choice'] retorna o ID da opção selecionada, como uma string. 
    # Os valores de request.POST são sempre strings.
    try:
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
