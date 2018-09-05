from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth import get_user_model

from rest_framework.views import csrf_exempt
from rest_framework.decorators import api_view

from .models import Choice, Question
from .presenter import PollsPresenter
from .sendemail import get_data_for_pdf, send_report
from django.template.loader import get_template

User = get_user_model()
DELETE = "delete"

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'objects'

    def get_queryset(self):
        question = Question.objects.order_by(PollsPresenter.ordering(self.request))[:PollsPresenter.count(self.request)]
        administrator = User.objects.filter(is_admin=1).first()
        return {'latest_question_list':question,'admin':administrator}

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['admin'] = User.objects.filter(is_admin=1).first()
        return context


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

# Leave the rest of the views (detail, results, vote) unchanged
@csrf_exempt
def add(request):
    PollsPresenter.add(request)
    return HttpResponseRedirect(reverse('polls:index'))

@csrf_exempt
def options(request):
    PollsPresenter.options(request)
    return HttpResponseRedirect(reverse('polls:index'))

@csrf_exempt
def delete(request):
    if request.POST.get('option','').lower() == DELETE:
        context = {'latest_question_list': Question.getQuestion(request.POST.getlist('id_list')),
        'admin':User.objects.filter(is_admin=1).first()}
        return render(request, 'polls/delete.html', context)
    return HttpResponseRedirect(reverse('polls:index'))

@csrf_exempt
def one_delete(request, question_id):
    if question_id:
        context = {'latest_question_list': Question.getQuestion(question_id),
        'admin':User.objects.filter(is_admin=1).first()}
        return render(request, 'polls/delete.html', context)
    return HttpResponseRedirect(reverse('polls:index'))

def show_email(request):
    question = Question.objects.all()
    administrator = User.objects.filter(is_admin=1).first()
    users = User.objects.filter(is_admin=0).order_by('-created')

    template = get_template('polls/pdf.html')
    html = template.render(get_data_for_pdf(administrator,question,''))

    context = {'users':users,'admin':administrator, 'template':html}
    return render(request, 'polls/sendemail.html', context)

@api_view(['POST', 'GET'])
@csrf_exempt
def send_email(request, email):
    question = Question.objects.all()
    administrator = User.objects.filter(is_admin=1).first()
    if request.POST.get('email',''):
        context = get_data_for_pdf(administrator, question, request.POST.get('email',''))
        return send_report('polls/pdf.html', context)
    return HttpResponseRedirect(reverse('polls:show_email'))