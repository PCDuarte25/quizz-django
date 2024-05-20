from django.contrib import messages
from django.db.models import F, ExpressionWrapper, DurationField, Q
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
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
        if 'answer' in request.POST:
            if person.current_question > question_number:
                penalize_cheater(person, context)
            elif person.current_question == question_number:
                # gir = Got It Right.
                gir = request.POST['answer'] == 'ans-2'
                add_person_score(person, gir)
                person.save()

                return redirect(reverse('question_1', kwargs={'person_id': person.id}) + f"?gir={1 if gir else 0}")
        else:
            messages.error(request, 'Você precisa selecionar pelo menos uma opção')

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
        if 'answer' in request.POST:
            if person.current_question > question_number:
                penalize_cheater(person, context)
            elif person.current_question == question_number:
                # gir = Got It Right.
                gir = request.POST['answer'] == 'ans-2'
                add_person_score(person, gir)
                person.save()

                return redirect(reverse('question_2', kwargs={'person_id': person.id}) + f"?gir={1 if gir else 0}")
        else:
            messages.error(request, 'Você precisa selecionar pelo menos uma opção')

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
        if 'answer' in request.POST:
            if person.current_question > question_number:
                penalize_cheater(person, context)
            elif person.current_question == question_number:
                # gir = Got It Right.
                gir = request.POST['answer'] == 'ans-3'
                add_person_score(person, gir)
                person.save()

                return redirect(reverse('question_3', kwargs={'person_id': person.id}) + f"?gir={1 if gir else 0}")
        else:
            messages.error(request, 'Você precisa selecionar pelo menos uma opção')

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
        if 'answer' in request.POST:
            if person.current_question > question_number:
                penalize_cheater(person, context)
            elif person.current_question == question_number:
                # gir = Got It Right.
                gir = request.POST['answer'] == 'ans-2'
                add_person_score(person, gir)
                person.save()

                return redirect(reverse('question_4', kwargs={'person_id': person.id}) + f"?gir={1 if gir else 0}")
        else:
            messages.error(request, 'Você precisa selecionar pelo menos uma opção')

    else:
        gir = request.GET.get('gir')
        add_after_answer_context('Comprar produtos a granel em vez de embalagens individuais', context, gir)

    return render(request, 'waste/question_4.html', context)


def question_5(request: HttpRequest, person_id: int) -> HttpResponse:
    question_number = 5
    person = get_object_or_404(Person, pk=person_id)
    context = build_context(question_number, person)

    if person.current_question < question_number:
       return redirect(f"question_{person.current_question}", person_id=person.id)

    if request.method == 'POST':
        print(request.POST)
        if person.current_question == question_number:
            battery_bin_item = request.POST.get('battery-bin')
            metal_bin_item = request.POST.get('metal-bin')
            organic_bin_item = request.POST.get('organic-bin')

            if (
                battery_bin_item
                and metal_bin_item
                and organic_bin_item
            ):
                is_correct = (
                    battery_bin_item == 'battery'
                    and metal_bin_item == 'soda'
                    and organic_bin_item == 'apple'
                )

                if is_correct:
                    person.score += 20

                person.quizz_end_time = timezone.now()
                person.save()

                return redirect(reverse('question_5', kwargs={'person_id': person.id}) + f"?gir={1 if is_correct else 0}")
            else:
                messages.error(request, 'Você precisa colocar todos os resíduos nas lixeiras')
    else:
        gir = request.GET.get('gir')
        add_after_answer_context('A lata é na lixeira amarela, a maçã é na lixeira marrom e a bateria é na lixeira laranja', context, gir)

    return render(request, 'waste/question_5.html', context)


def ranking(request: HttpRequest, person_id: int|None = None) -> HttpResponse:
    qs = Person.objects.filter(quizz_end_time__isnull=False).annotate(
        finished_quizz_time=ExpressionWrapper(F('quizz_end_time') - F('quizz_start_time'), output_field=DurationField())
    )

    top_people_qs = qs.order_by('-score', 'finished_quizz_time')

    context = {'range': range(10)}

    top_people = list(top_people_qs[0:10])

    if person_id is not None:
        person = get_object_or_404(Person, pk=person_id)
        context['current_person'] = person

        position = qs.filter(
            Q(score__gt=person.score)
            | (Q(score=person.score) & Q(finished_quizz_time__lt=person.get_finished_quizz_time))
        ).count() + 1

        if position > 10:
            top_people[len(top_people) - 1] = person

        context['current_person_position'] = position

    context['top_people'] = top_people

    return render(request, 'waste/ranking.html', context)

def progress_bar_class(question_number):
    if question_number == 5:
        return 'is-success'
    else:
        return 'is-primary'


def build_context(question_number, person):
    context = {
        'current_question': question_number,
        'progress_pct': (question_number / 5) * 100,
        'progress_bar_class': progress_bar_class(question_number),
        'person': person,
    }

    if question_number == 5:
        context['next_page_url'] = reverse(f"person_ranking", kwargs={'person_id': person.id})
    else:
        context['next_page_url'] = reverse(f"question_{question_number + 1}", kwargs={'person_id': person.id})

    return context

def penalize_cheater(person, context):
    context['is_cheating'] = True
    context['person_current_question_url'] = get_person_current_question_url(person)
    person.score -= 20
    person.save()


def add_person_score(person, gir):
    person.current_question += 1
    if gir:
        person.score += 20


def add_after_answer_context(answer, context, gir):
    if gir is not None:
        context['gir'] = gir
        if gir != '1':
            context['correct_answer'] = answer


def get_person_current_question_url(person):
    return reverse(f"question_{person.current_question}", kwargs={'person_id': person.id})
