# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
# get returns the first match 1 and only 1
# filter returns a set of matches, and you need to select(array operations)

class Publisher(models.Model): # a subclass of django.db.models.Model
	name = models.CharField(max_length=30)
	address = models.CharField(max_length=50)
	city = models.CharField(max_length=60)
	state_province = models.CharField(max_length=30)
	country = models.CharField(max_length=50)
	website = models.URLField()

	def __str__(self):
		return self.name + ' from ' + self.city + ' (' + self.state_province + ', ' + self.country + ')'

class Author(models.Model):
	salutation = models.CharField(max_length=10)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=40)
	email = models.EmailField()
	age = models.IntegerField(default=16)
	#headshot = models.ImageField(upload_to='/tmp')	
	def __str__(self):
		return '%s , %s' % (self.first_name, self.last_name)

class Book(models.Model):
	title = models.CharField(max_length=100)
	authors = models.ManyToManyField(Author)
	publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
	publication_date = models.DateField(auto_now_add=True, blank=True)
	popularity = models.FloatField(default=0.6)

	def __str__(self):
		return self.title
	class Meta:
		ordering = ['title']