from django.shortcuts import render, redirect
from .models import Decision
from .forms import DecisionForm

# Create your views here.

def home(request):
    decisions = Decision.objects.all()
    context = {'decisions': decisions}
    return render(request, 'warmth/home.html', context)


def decision(request, pk):
    decision = Decision.objects .get(id=pk)
    context = {'decision': decision}
    return render(request, 'warmth/decision.html', context)


def createDecision(request):
    form = DecisionForm()
    if request.method == 'POST':
        form = DecisionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'warmth/decision_form.html', context)

def updateDecision(request, pk):
    decision = Decision.objects.get(id=pk)
    form = DecisionForm(instance=decision)

    if request.method == 'POST':
        form = DecisionForm(request.POST, instance=decision)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'warmth/decision_form.html', context)