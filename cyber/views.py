from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from .models import Note
import sys
import sqlite3
import string

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


