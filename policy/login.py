from django.core.cache import cache
from django.shortcuts import redirect

def cookies_login(fun):
	def auth(request, *args, **kwargs):
		if 'token' not in request.COOKIES:
			return redirect('/login/')
		login_check = cache.get(request.COOKIES['token'])
		if login_check == None:
			return redirect('/login/')
		return fun(request, *args, **kwargs)
	return auth