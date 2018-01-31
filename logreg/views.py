# _*_ coding: utf-8 _*_
from django.shortcuts import render, redirect
from .forms import RegisterForm

# Create your views here.
def register(request):
    redirect_to = request.POST.get('next', request.GET.get('next',''))
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'logreg/register.html',context={'form':form})

def index(request):
    return render(request,'index.html')