from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from django.contrib.auth.models import User, Group
from users.forms import UserCreateForm, UserEditForm

# Create your views here.


def index(request):
	return render(request, 'users/index.html')

@login_required
def user_list(request):
	group = Group.objects.get(name='std_user')
	user_list = group.user_set.all().order_by('username')
	return render(request, 'users/user_list.html', {'user_list': user_list})


def register(request):
	if request.method == "POST":
		form = UserCreateForm(data=request.POST)
		if form.is_valid():
			user = form.save()
			return HttpResponseRedirect("/users/login")
		else:
			print form.errors
	else:
		form = UserCreateForm()
	return render(request, 'users/user_form.html', {'form': form, 
		'form_type': 'register'})


@login_required
def add_user(request):
	if request.method == "POST":
		form = UserCreateForm(data=request.POST)
		if form.is_valid():
			user = form.save()
			return HttpResponseRedirect("/users/user_list")
		else:
			print form.errors
	else:
		form = UserCreateForm()
	return render(request, 'users/user_form.html', {'form': form, 
		'form_type': 'add'})	


@login_required
def user_edit(request, username):	
	user = get_object_or_404(User, username=username)
	if request.method == "POST":
		form = UserEditForm(request.POST, instance=user)
		if form.is_valid():
			if request.POST.get('delete'):
				user.delete()
			else:
				form.save()
			return HttpResponseRedirect("/users/user_list")
	else:
		form = UserEditForm(instance=user)
	return render(request, 'users/user_form.html', {'form': form, 
		'form_type': 'edit'})


def user_login(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/users/user_list')
			else:
				return HttpResponse("Account is disabled.")
		else:
			print "Invalid login information: {0}, {1}".format(username, 
				password)
			return HttpResponse("Invalid login information.")
	else:
		return render(request, 'users/login.html', {})


@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/users/')