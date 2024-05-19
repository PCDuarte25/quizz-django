from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import PersonForm
from .models import Person

# Create your views here.
def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request, 'waste/dashboard.html')


def user(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = PersonForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('question_1', person_id=form.instance.id)
    else:
        form = PersonForm()

    return render(request, 'waste/user.html', {'form': form})


def question_1(request: HttpRequest, person_id: int) -> HttpResponse:
    question_number = 1
    person = get_object_or_404(Person, pk=person_id)
    context = build_context(question_number, person)

    if request.method == 'POST':
        if person.current_question > question_number:
            penalize_cheater(person, context)
        elif person.current_question == question_number:
            # gir = Got It Right.
            gir = request.POST['answer'] == 'ans-2'
            add_person_score(person, gir)

            return redirect(reverse('question_1', kwargs={'person_id': person.id}) + f"?gir={1 if gir else 0}")
    else:
        gir = request.GET.get('gir')
        add_after_answer_context('Reciclagem', context, gir)

    return render(request, 'waste/question_1.html', context)


def question_2(request: HttpRequest, person_id: int) -> HttpResponse:
    question_number = 2
    person = get_object_or_404(Person, pk=person_id)
    context = build_context(question_number, person)

    if person.current_question < question_number:
       return redirect(f"question_{person.current_question}", person_id=person.id)

    if request.method == 'POST':
        if person.current_question > question_number:
            penalize_cheater(person, context)
        elif person.current_question == question_number:
            # gir = Got It Right.
            gir = request.POST['answer'] == 'ans-2'
            add_person_score(person, gir)

            return redirect(reverse('question_2', kwargs={'person_id': person.id}) + f"?gir={1 if gir else 0}")
    else:
        gir = request.GET.get('gir')
        add_after_answer_context('Separar materiais recicláveis dos não recicláveis', context, gir)

    return render(request, 'waste/question_2.html', context)


def question_3(request: HttpRequest, person_id: int) -> HttpResponse:
    question_number = 3
    person = get_object_or_404(Person, pk=person_id)
    context = build_context(question_number, person)

    if person.current_question < question_number:
       return redirect(f"question_{person.current_question}", person_id=person.id)

    if request.method == 'POST':
        if person.current_question > question_number:
            penalize_cheater(person, context)
        elif person.current_question == question_number:
            # gir = Got It Right.
            gir = request.POST['answer'] == 'ans-3'
            add_person_score(person, gir)

            return redirect(reverse('question_3', kwargs={'person_id': person.id}) + f"?gir={1 if gir else 0}")
    else:
        gir = request.GET.get('gir')
        add_after_answer_context('Reciclá-los em instalações apropriadas', context, gir)

    return render(request, 'waste/question_3.html', context)


def question_4(request: HttpRequest, person_id: int) -> HttpResponse:
    question_number = 4
    person = get_object_or_404(Person, pk=person_id)
    context = build_context(question_number, person)

    if person.current_question < question_number:
       return redirect(f"question_{person.current_question}", person_id=person.id)

    if request.method == 'POST':
        if person.current_question > question_number:
            penalize_cheater(person, context)
        elif person.current_question == question_number:
            # gir = Got It Right.
            gir = request.POST['answer'] == 'ans-2'
            add_person_score(person, gir)

            return redirect(reverse('question_4', kwargs={'person_id': person.id}) + f"?gir={1 if gir else 0}")
    else:
        gir = request.GET.get('gir')
        add_after_answer_context('Comprar produtos a granel em vez de embalagens individuais', context, gir)

    return render(request, 'waste/question_4.html', context)


def question_5(request: HttpRequest, person_id: int) -> HttpResponse:
    current_question = 5
    person = get_object_or_404(Person, pk=person_id)

    return render(request, 'waste/question_5.html', {
        'current_question': current_question,
        'progress_pct': (current_question / 5) * 100,
        'progress_bar_class': progress_bar_class(current_question),
        'person': person,
    })


def progress_bar_class(question_number):
    if question_number == 5:
        return 'is-success'
    else:
        return 'is-primary'


def build_context(question_number, person):
    return {
        'current_question': question_number,
        'progress_pct': (question_number / 5) * 100,
        'progress_bar_class': progress_bar_class(question_number),
        'person': person,
        'next_page_url': reverse(f"question_{question_number + 1}", kwargs={'person_id': person.id})
    }

def penalize_cheater(person, context):
    context['is_cheating'] = True
    context['person_current_question_url'] = get_person_current_question_url(person)
    person.score -= 20
    person.save()


def add_person_score(person, gir):
    person.current_question += 1
    if gir:
        person.score += 20
    person.save()


def add_after_answer_context(answer, context, gir):
    if gir is not None:
        context['gir'] = gir
        if gir != '1':
            context['correct_answer'] = answer


def get_person_current_question_url(person):
    return reverse(f"question_{person.current_question}", kwargs={'person_id': person.id})
