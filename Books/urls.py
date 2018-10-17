from django.urls import path
from . import views

app_name = 'Books'
urlpatterns = [
	path('', views.index, name='index'),
	path('authorid/<int:author_id>/', views.detail, name='detail'),#no space is allowed within <>
	path('authorid/<int:author_id>/results/', views.results, name='results'),
	path('authorid/<int:author_id>/vote/', views.vote, name='vote'),
	path("login", views.login_view, name="login"), #'django.contrib.auth.views.login' 
    path("signup", views.signup, name="signup"),
    path("logout", views.logout_view, name="logout"),
    #path("portfolio", views.portfolio, name="portfolio"),
]