from django.shortcuts import render
from .forms import InputForm

from .algo import recommend

def home(request):
    template = "home.html"
    context = {}
    return render(request, "home.html", context)

def quiz(request):
    if request.method == 'POST':
        recs = recommend(request.POST)
        context = {'results': recs.values.tolist()}
        return render(request, 'results.html', context)
    context = {}
    context['form']= InputForm()
    return render(request, "quiz.html", context)
