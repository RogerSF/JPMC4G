# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse

from .models import *

def index(request):
	author_list = Author.objects.order_by('first_name')[:5]
	context = { # always a dictionary
		'author_list': author_list,
	}
	return render(request, 'Books/index.html', context)

def detail(request, author_id):
	# try:
	# 	author = Author.objects.get(id=book_id)
	# 	context = {
	# 		'author':  author
	# 	}
	# except Author.DoesNotExist:
	# 	raise Http404('The author you requsted does not exist')
	# return render(request, 'Books/detail.html', context)
	author = get_object_or_404(Author, id=author_id)
	return render(request, 'Books/detail.html', {'author': author})

def results(request, author_id):
	author = get_object_or_404(Author, id=author_id)
	return render(request, 'Books/results.html', {'author': author})

def vote(request, author_id):
	# if the method is a POST, a redirect operation is always expected to avoid error 
	author = get_object_or_404(Author, id=author_id)
	try:
		selected_book = author.book_set.get(id=request.POST['book'])
	except (KeyError, Book.DoesNotExist):#implicitly if
		return render(request, 'Books/detail.html', {'author': author, 'error_message': 'You have not yet select a Book'})
	else:#no KeyError
		selected_book.popularity += 0.01
		selected_book.save()
		return HttpResponseRedirect(reverse('Books:results', args=(author.id,)))#redirect to voting result page
	
