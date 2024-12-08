from django.shortcuts import render, redirect
from .forms import HumanForm
from .models import Human
# Create your views here.


def index(request):
    humans = Human.objects.order_by('-id')
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {'title': 'Главная страница сайта', 'humans': humans, 'num_visits': num_visits}
    return render(request, 'index.html', context)


def create(request):
    error = ''
    if request.method == 'POST':
        form = HumanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = "Форма была не верной"
    form = HumanForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'create.html', context)

def human_list(request):
    humans = Human.objects.order_by('-id')
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    if request.method == 'POST':
        form = HumanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('human_list')  # Перенаправление после сохранения
    else:
        form = HumanForm()

    context = {
        'title': 'Главная страница сайта',
        'humans': humans,
        'num_visits': num_visits,
        'form': form,
    }
    
    return render(request, 'human_list.html', context)
