from django.shortcuts import render

from .forms import *
from .models import *
# Create your views here.

def new_post(request):
	template = '/create-post.html'
	form = PostForm(request.POST)

	if form.is_valid():
		form.save()

	else:
		form = PostForm()

	context = {
		'form' : form,
	}	
	return render(request, template, context)