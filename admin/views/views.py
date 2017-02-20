from django.shortcuts import render, redirect
from django.template import loader, Context
from django.http import HttpResponseRedirect
from commonlib.models import User,Post,Photo
from django.core.cache import cache
from policy.login import cookies_login
import hashlib, logging, time
 
logger = logging.getLogger(__name__)

def notDefinedUrl(request):
	return redirect('/login')

def login(request):

	if request.method == 'GET':
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

			cache.set(hash_account.hexdigest(), account_info, 300)
			response = HttpResponseRedirect('/admin/')
			response.set_cookie('token', hash_account.hexdigest())

			logger.info(account_info.name+" login at "+time.strftime("%d/%m/%Y %H:%M:%S"))

			return response
		else:
			return render(request, 'login.html', {'err_msg': 'password or account error',})

@cookies_login
def logout(request):
	cache.delete(request.COOKIES['token'])
	return redirect('/login')

@cookies_login
def admin(request):

	return render(request, 'index.html')

@cookies_login
def postList(request):
	if request.method == 'GET':
		post_list = Post.objects.all()
		return render(request, 'post_list.html', {
			'post_list': post_list
		})

@cookies_login
def newPost(request):
	if request.method == 'GET':
		return render(request, 'post_detail.html' )
	else:

		user_dict = cache.get(request.COOKIES['token'])
	
		post = Post()
		post.title = request.POST.get('title')
		post.description = request.POST.get('description')
		post.text = request.POST.get('text')
		post.location = request.POST.get('location')
		post.user_id = user_dict.id
		post.date = request.POST.get('date')
		post.save()

		image_data = request.FILES.get('image')
		
		if image_data.name.endswith('.jpg'):
			local_name = str(time.time()) + '.jpg'
		elif image_data.name.endswith('.png'):
			local_name = str(time.time()) + '.png'
		elif image_data.name.endswith('.gif'):
			local_name = str(time.time()) + '.gif'
		else:
			return redirect(request.META().get('HTTP_REFERER', '/'))
		F = open('/admin/upload/' + local_name, 'wb')
		for line in image_data:
			F.write(line)
		F.close()

		photo = Photo()
		photo.url = local_name
		photo.post_id = post.id
		photo.save()

		return redirect('/admin/post/list')

@cookies_login
def postDetail(request, id):
	post = Post.objects.get(id=id)
	photo_list = Photo.objects.filter(post_id=post.id)

	return render(request, 'post_detail.html', {
		'post': post,
		'photo_list': photo_list
	})

@cookies_login
def postUpdate(request, id):
	post = Post.objects.get(id=id)

	post.title = request.POST.get('title')
	post.description = request.POST.get('description')
	post.text = request.POST.get('text')
	post.location = request.POST.get('location')
	post.date = request.POST.get('date')
	post.save()

	return redirect('/admin/post/'+id+'/')

@cookies_login
def postDelete(request, id):
	post = Post.objects.get(id=id)
	post.delete()
	return redirect('/admin/post/list')