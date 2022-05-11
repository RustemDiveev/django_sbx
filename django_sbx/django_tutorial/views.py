from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic 

from .models import Question, Choice

# Create your views here.

def index(request):
    """
        Простейшее представление
    """
    return HttpResponse("Blablabla")

def detail(request, question_id):
    """
        Просмотр вопроса 
    """
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    """
        Результаты вопроса 
    """
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    """
        ГОЛОСОВАНИЕ
    """
    return HttpResponse("You're voting on question %s." % question_id)

def index_last_5(request):
    """
        Последние 5 вопросов 
    """
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    output = ", ".join([q.question_text for q in latest_question_list])
    return HttpResponse(output)

def index_last_5_templated(request):
    """
        Последние 5 вопросов, но с шаблоном 
    """
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        "latest_question_list": latest_question_list
    }

    """
    template = loader.get_template("django_tutorial/index_last_5_templated.html")
    return HttpResponse(template.render(context, request))
    """

    # синтаксический сахар
    return render(request, template_name="django_tutorial/index_last_5_templated.html", context=context)

def detail_templated(request, question_id):
    """
        Детальное представление вопроса с использованием шаблона 
        и проверкой существования объекта 
    """

    """
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question doesn't exist")
    """

    # синтаксический сахар 
    # Пока не понятно, как управлять текстом ошибки 
    question = get_object_or_404(Question, pk=question_id)

    return render(
        request=request,
        template_name="django_tutorial/detail_templated.html",
        context={"question": question}
    )

def detail_form(request, question_id):
    """
        Детальное представление вопроса с шаблоном и возможностью голосования 
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(
        request=request,
        template_name="django_tutorial/detail_form.html",
        context={"question": question}
    )

def vote_form(request, question_id):
    """
        Голосование с использованием шаблона, где есть форма 
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST - словарь того, что отправлено с веб-формы 
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request=request,
            template_name="django_tutorial/detail_form.html",
            context={
                "question": question,
                "error_message": "You didn't select a choice"
            }
        )
    else:
        selected_choice.votes += 1 
        selected_choice.save()
        # Всегда необходимо возвращать HttpResponseDirect после выполнения POST-запроса, 
        # чтобы не сабмитить одну форму несколько раз 
        return HttpResponseRedirect(reverse(
            "django_tutorial:results_templated",
            args=(question_id,)
        ))

def results_templated(request, question_id):
    """
        Результаты голосования с использованием шаблона 
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "django_tutorial/results_templated.html", {"question": question})