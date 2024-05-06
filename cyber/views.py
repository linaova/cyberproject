from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib.auth import login, authenticate, logout

from .models import Note


@login_required
def deleteView(request):

	f = Note.objects.get(pk=request.POST.get('id'))
	f.delete()
	return redirect('/')

	#try: 
    #	f = Note.objects.get(pk=request.POST.get('id'), user = request.user)
    #	f.delete()
    #except:
    #pass
    #return redirect('/')

	
	

@login_required
def addView(request):
	note = request.POST.get('note')

	f = Note(user=request.user, note=note)
	f.save()
	return redirect('/')


@login_required
def homePageView(request):
	user_notes = Note.objects.raw('SELECT * FROM cyber_note WHERE user_id = %s' % request.user.id)
	# user_notes = Note.objects.filter(user=request.user)
	return render(request, 'cyber/index.html', {'user_notes': user_notes})


def signUpView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'cyber/signup.html', {'form': form})

def logOutView(request):
    logout(request)
    return redirect('/')