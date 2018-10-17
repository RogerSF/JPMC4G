# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


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
	

# def portfolio(request):
#     if request.user.is_authenticated:
#         if request.method == 'GET':
#             # Construct Portfolio from a User's Positions
#             portfolio = Position.objects.filter(user=request.user)
#             if len(portfolio) == 0:
#                 return render(request, 'portfolio/portfolio.html', {'user': request.user})
#             portfolio_to_send = {}
#             portfolio_overall = {'initial_portfolio_value_usd': 0, 'current_portfolio_value_usd': 0}
#             crypto_codes = ''
#             # Prepare Crypto code string for API GET request and initialize actual data structure to be sent to
#             # portfolio page--portfolio_to_send
#             for position in portfolio:
#                 crypto_codes += position.crypto.code + ','
#                 key = f'{position.crypto.code}-{position.id}'
#                 portfolio_to_send[key] = {'id': position.id, 'name': position.crypto.name, 'code': position.crypto.code,
#                                           'quantity': position.quantity, 'price_purchased_usd': position.price_purchased_usd
#                 }
#                 initial_position_value = round(position.quantity * position.price_purchased_usd, 2)
#                 portfolio_overall['initial_portfolio_value_usd'] += float(initial_position_value)

#             # GET live data
#             api_request = f'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={crypto_codes}&tsyms=USD,BTC'
#             crypto_portfolio_data = requests.get(api_request).json()['RAW']

#             # Fill portfolio_to_send with live data from API GET request
#             for position in portfolio_to_send:

#                 # Price of asset in USD and BTC
#                 usd_price = round(crypto_portfolio_data[position.split('-')[0]]['USD']['PRICE'], 4)
#                 portfolio_to_send[position]['usd_price'] = '{:,}'.format(Decimal(usd_price).quantize(Decimal(10) ** -2))
#                 portfolio_to_send[position]['btc_price'] = crypto_portfolio_data[position.split('-')[0]]['BTC']['PRICE']

#                 # Value of position in USD and BTC
#                 usd_value = round(usd_price *  float(portfolio_to_send[position]['quantity']), 2)
#                 btc_value = round(portfolio_to_send[position]['btc_price'] *  float(portfolio_to_send[position]['quantity']), 2)
#                 portfolio_to_send[position]['usd_value'] = '{:,}'.format(Decimal(usd_value).quantize(Decimal(10) ** -2))
#                 portfolio_to_send[position]['btc_value'] = btc_value

#                 # 24h Percent Change with respect to USD and BTC
#                 portfolio_to_send[position]['change_pct_24h_usd'] = round(crypto_portfolio_data[position.split('-')[0]]['USD']['CHANGEPCT24HOUR'], 2)
#                 portfolio_to_send[position]['change_pct_24h_btc'] = round(crypto_portfolio_data[position.split('-')[0]]['BTC']['CHANGEPCT24HOUR'], 2)

#                 # 24h Position Value Change in USD and BTC
#                 portfolio_to_send[position]['change_value_24h_usd'] = '{:,}'.format(Decimal(usd_value * (portfolio_to_send[position]['change_pct_24h_usd']/100.0)).quantize(Decimal(10) ** -2))
#                 portfolio_to_send[position]['change_value_24h_btc'] = round(portfolio_to_send[position]['btc_value'] * (portfolio_to_send[position]['change_pct_24h_btc']/100.0), 10)

#                 # Position Percent Change since Purchase in USD
#                 portfolio_to_send[position]['change_pct_since_purchase_usd'] =  '{:,}'.format(round(((( usd_price / float(portfolio_to_send[position]['price_purchased_usd']) ) - 1) * 100), 2))

#                 # Add to current portfolio value in USD
#                 portfolio_overall['current_portfolio_value_usd'] += usd_value

#             portfolio_overall['current_portfolio_value_usd'] = Decimal(portfolio_overall['current_portfolio_value_usd']).quantize(Decimal(10) ** -2)
#             portfolio_overall['return_overall_percent_usd'] = round(((float(portfolio_overall['current_portfolio_value_usd']) / portfolio_overall['initial_portfolio_value_usd'])-1)*100.0, 2)
#             return_overall_percent_usd = '{:,}'.format(portfolio_overall['return_overall_percent_usd'])
#             portfolio_overall['return_overall_percent_usd'] = f'{return_overall_percent_usd}%'
#             portfolio_overall['current_portfolio_value_usd'] = '{:,}'.format(portfolio_overall['current_portfolio_value_usd'])

#             if request.is_ajax():
#                 context = {
#                     'success': True,
#                     'portfolio_to_send': portfolio_to_send,
#                     'portfolio_overall': portfolio_overall
#                 }
#                 response = JsonResponse(context)
#                 add_never_cache_headers(response)
#                 return response
#             else:
#                 context = {
#                     'portfolio': portfolio_to_send,
#                     'overall': portfolio_overall,
#                     'user': request.user
#                 }
#                 return render(request, 'portfolio/portfolio.html', context)

#         try:
#             if request.is_ajax() and request.POST['action'] == 'add-new-position':
#                 position_to_send = {}
#                 code = request.POST['code'];
#                 quantity = float(request.POST['quantity'])
#                 price_purchased_usd = float(request.POST['price_purchased_usd'])
#                 date = request.POST['date']

#                 # Add position to DB Model for user
#                 crypto = Crypto.objects.get(code=code)
#                 new_position = Position(user=request.user, crypto=crypto, quantity=quantity, price_purchased_usd=price_purchased_usd, date_purchased=date)
#                 quantity = new_position.quantity
#                 price_purchased_usd = new_position.price_purchased_usd
#                 new_position.save()

#                 # GET live data
#                 api_request = f'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={code}&tsyms=USD,BTC'
#                 crypto_portfolio_data = requests.get(api_request).json()['RAW']

#                 # Price in USD and BTC
#                 usd_price = round(crypto_portfolio_data[code]['USD']['PRICE'], 4)
#                 btc_price = crypto_portfolio_data[code]['BTC']['PRICE']

#                 # Value of Position in USD and BTC
#                 usd_value = round(usd_price * float(quantity), 2)
#                 btc_value = btc_price * float(quantity)

#                 # 24h Percent Change with respect to USD and BTC
#                 change_pct_24h_usd = round(crypto_portfolio_data[code]['USD']['CHANGEPCT24HOUR'], 2)
#                 change_pct_24h_btc = round(crypto_portfolio_data[code]['BTC']['CHANGEPCT24HOUR'], 2)

#                 # 24h Position Value Change in USD and BTC
#                 change_value_24h_usd = round((change_pct_24h_usd/100.0) * usd_value, 2)
#                 change_value_24h_btc = (change_pct_24h_btc/100.0) * btc_value

#                 # Position Percent Change since Purchase in USD
#                 change_pct_since_purchase_usd = round(((usd_price/float(price_purchased_usd))-1)*100.0,2)

#                 position_to_send = {'success': True,
#                                     'name': crypto.name, 'code': code,
#                                     'quantity': quantity, 'price_purchased_usd': price_purchased_usd,
#                                     'usd_price': usd_price, 'btc_price': btc_price, 'usd_value': usd_value,
#                                     'btc_value': btc_value, 'change_pct_24h_usd': change_pct_24h_usd,
#                                     'change_pct_24h_btc': change_pct_24h_btc, 'change_value_24h_usd': change_value_24h_usd,
#                                     'change_value_24h_btc': change_value_24h_btc,
#                                     'change_pct_since_purchase_usd': change_pct_since_purchase_usd
#                 }
#                 return JsonResponse(position_to_send)
#             elif request.is_ajax() and request.POST['action'] == 'delete-positions':
#                 positions_to_delete = request.POST['positions_to_delete'].split(',')
#                 for position_id in positions_to_delete:
#                     position = Position.objects.get(id=position_id)
#                     position.delete()
#                 return JsonResponse({'success': True})
#         except Exception as e:
#             return JsonResponse({'success': False})
#     else:
#         return redirect('login')







#Authentication Procedure
def login_view(request):
    if request.method == 'GET': #loading the log in page
        return render(request, 'Books/login.html')
    if not request.user.is_authenticated:
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None: # a valid user
                login(request, user)
                return redirect('Books:index')#portfolio
            else: # a invalid user
                return render(request, 'Books/login.html', {'message': "Invalid Credentials"})
        except Exception as e:
            print(e)
            return render(request, 'Books/login.html', {'message': "Invalid Credentials"})
    else:#when cached user re-visit
        return redirect('Books:index')#portfolio

def signup(request):
    if request.method == 'GET':
        return render(request, 'Books/signup.html')
    if not request.user.is_authenticated:
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            new_user = User.objects.create_user(username=username, email=email, password=password)
            if new_user is not None:
                return redirect('Books:login')
            else:
                return render(request, 'portfolio/signup.html', {'message': "Invalid Credentials"})
        except Exception as e:
            return render(request, 'portfolio/signup.html', {'message': "Invalid Credentials"})
    else:
        return redirect('Books:login')#portfolio

def logout_view(request):
    logout(request)
    return redirect('Books:index')


# class IndexView(generic.ListView):
# 	template_name = 'Books/index.html'
# 	context_object_name = 'author_list'

# 	def get_query(self):
# 		return Author.obejcts.order_by('age')

# class DetailView(generic.DetailView):
# 	model = Author
# 	template_name = 'Books/detail.html'

# class ResultView(generic.DetailView):
# 	model = Author
# 	template_name = 'Books/result.html'
