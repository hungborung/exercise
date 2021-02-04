from django.shortcuts import render, redirect

# Create your views here.


from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import MyUserCreationForm


def signup(request):    
    form = MyUserCreationForm()
   
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.username,
                                password=request.POST['password1'] )
            login(request, user)
            return redirect('home')
            
    return render(request, 'signup.html', { 'form':  form})


@login_required
def account(request):
    return render(request, 'profile/general.html')

@login_required
def userorder(request):
    return render(request, 'profile/userorder.html')
    
@login_required
def notification(request):
    return render(request, 'profile/notification.html')