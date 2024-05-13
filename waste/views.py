from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def dashboard(request):
    return render(request, 'waste/dashboard.html')


def user(request):
    return render(request, 'waste/user.html')


def question_1(request):
    current_question = 1

    return render(request, 'waste/question_1.html', {
        'current_question': current_question,
        'progress_pct': (current_question / 5) * 100,
        'progress_bar_class': progress_bar_class(current_question),
    })


def question_2(request):
    current_question = 2

    return render(request, 'waste/question_2.html', {
        'current_question': current_question,
        'progress_pct': (current_question / 5) * 100,
        'progress_bar_class': progress_bar_class(current_question),
    })


def question_3(request):
    current_question = 3

    return render(request, 'waste/question_3.html', {
        'current_question': current_question,
        'progress_pct': (current_question / 5) * 100,
        'progress_bar_class': progress_bar_class(current_question),
    })


def question_4(request):
    current_question = 4

    return render(request, 'waste/question_4.html', {
        'current_question': current_question,
        'progress_pct': (current_question / 5) * 100,
        'progress_bar_class': progress_bar_class(current_question),
    })


def question_5(request):
    current_question = 5

    return render(request, 'waste/question_5.html', {
        'current_question': current_question,
        'progress_pct': (current_question / 5) * 100,
        'progress_bar_class': progress_bar_class(current_question),
    })


def progress_bar_class(question_number):
    if question_number == 5:
        return 'is-success'
    else:
        return 'is-primary'
