# trips/views.py

from datetime import datetime
from django.shortcuts import render
from django.template import loader, Context
from django.http import HttpResponse
from commonlib.models import User
from django.core.cache import cache
import hashlib
 

def login(request):
	if request.method == 'GET':
		return HttpResponse(request.COOKIES)
		if 'login' in request.COOKIES:
			hash_account = request.COOKIES['login']
			response = HttpResponse(hash_account.hexdigest())
			return response
		return render(request, 'login.html')
	
	elif request.method == 'POST':		
		account = request.POST.get('account', '')
		password = request.POST.get('password', '')
		
		try:
			account_info = User.objects.get(account=account)
		except User.DoesNotExist:
			account_info = None

		if account_info != None and password == account_info.password:
			hash_account = hashlib.md5(account)

			cache.set(hash_account.hexdigest(), 'login', 30)
			response = HttpResponse(hash_account.hexdigest())
			response.set_cookie('login', hash_account.hexdigest())
			return response
		else:
			return render(request, 'login.html', {'err_msg': 'password or account error',})