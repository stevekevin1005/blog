from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.core.cache import cache
from policy.login import token_login
from commonlib.models import User, Post, Photo, Comment, Like, Participate

import json, datetime

def login(request):
		
	if request.method == 'POST':		
		account = request.POST.get('account', '')
		password = request.POST.get('password', '')

		try:
			account_info = User.objects.get(account=account)
		except User.DoesNotExist:
			account_info = None

		response = dict()

		if account_info != None and password == account_info.password:
			hash_account = hashlib.md5(account)
			cache.set(hash_account.hexdigest(), account_info, 30)
			
			response['status'] = 'success'
			response['token'] = hash_account.hexdigest()
			response['msg'] = 'Login success'

			return JsonResponse(response)
		
		else:

			response['status'] = 'error'
			response['token'] = None
			response['msg'] = 'Account or password error'
			
			return JsonResponse(response)

	else:
		return HttpResponse(status = 404)

@token_login
def postList(request):
	
	if request.method == 'GET':

		start_day = request.GET.get('start_day', '2000-01-01')
		end_day = request.GET.get('end_day', '2099-01-01')

		response = cache.get('post_list_'+start_day+"_"+end_day)
		if response == None:
			post_list = Post.objects.filter(date__range = [start_day, end_day])
			photo_list = Photo.objects.all()
			like_list = Like.objects.all()
			participate_list = Participate.objects.all()
			comment_list = Comment.objects.all()

			response = dict()
			response['status'] = 'success'
			response['post_list'] = []

			for post in post_list:
				post_data = dict()
				post_data['id'] = post.id
				post_data['description'] = post.description
				post_data['text'] = post.text
				post_data['location'] = post.location
				post_data['user_id'] = post.user_id
				post_data['date'] = post.date
				post_data['photo_list'] = []
				post_data['participate_list'] = []
				post_data['like_list'] = []
				post_data['comment_list'] = []

				for photo in photo_list:
					if photo.post_id == post.id:
						photo_data = dict()
						photo_data['url'] = photo.url
						post_data['photo_list'].append(photo_data)

				for participate in participate_list:
					if participate.post_id == post.id:
						participate_data = dict()
						participate_data['user_id'] = participate.user_id
						post_data['participate_list'].append(participate_data)

				for like in like_list:
					if like.post_id == post.id:
						like_data = dict()
						like_data['user_id'] = like.user_id
						post_data['like_list'].append(like_data)

				for comment in comment_list:
					if comment.post_id == post.id:
						comment_data = dict()
						comment_data['user_id'] = comment.user_id
						comment_data['text'] = comment.text
						post_data['comment_list'].append(like_data)

				response['post_list'].append(post_data)
				response['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				cache.set('post_list_'+start_day+"_"+end_day, response, 30)

		return JsonResponse(response)

	else:
		return HttpResponse(status = 404)

@token_login
def like(request, id):
	if request.method == 'GET':	
		user_dict = cache.get(request.META['token'])
		like, created = Like.objects.get_or_create(user_id=user_dict.id, post_id=id)

		if not created:
			like.delete()

		response = dict()
		response['status'] = 'success'
		response['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		return JsonResponse(response)

	else:
		return HttpResponse(status = 404)

@token_login
def participate(request, id):
	if request.method == 'GET':	
		user_dict = cache.get(request.META['token'])
		participate, created = Participate.objects.get_or_create(user_id=user_dict.id, post_id=id)

		if not created:
			participate.delete()

		response = dict()
		response['status'] = 'success'
		response['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		return JsonResponse(response)

	else:
		return HttpResponse(status = 404)

@token_login
def comment(request, id):
	if request.method == 'POST':	
		user_dict = cache.get(request.META['token'])
		comment = Comment()
		comment.post_id = id
		comment.user_id = user_dict.id
		comment.text = request.POST.get('text')
		comment.save()

		response = dict()
		response['status'] = 'success'
		response['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		return JsonResponse(response)

	else:
		return HttpResponse(status = 404)
