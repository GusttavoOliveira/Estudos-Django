from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader
from .models import Question

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
    response = "You're looking at the results of question %s" 
    return HttpResponse(response % question_id) 

def vote(request, question_id):
    return HttpResponse("You're voting on question %s" %question_id)
