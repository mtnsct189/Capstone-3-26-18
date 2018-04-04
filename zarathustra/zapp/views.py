from django.shortcuts import render, reverse, redirect

from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User, Group, Permission

from django.contrib.auth.decorators import login_required

from .models import List


# @login_required
def index(request):
    return render(request, 'zapp/index.html')


def registration_login(request):
    if 'logout' in request.GET.keys():
        message = 'You have successfully logged out.'
    if 'redirect' in request.GET.keys():
        message = 'You must log in to view this page.'

    next = request.GET.get('next', '')

    return render(request, 'zapp/registration_login.html', {'message': message, 'next': next})


def register(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    user = User.objects.create_user(username, email, password)

    group = Group.objects.get(name='todo editor')
    user.groups.add(group)
    user.save()

    login(request, user)

    return HttpResponse('zapp:register')


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        if 'next' in request.GET.keys():
            return HttpResponseRedirect(request.GET['next'])
        else:
            return HttpResponseRedirect(reverse('zapp:index'))
    else:
        return HttpResponseRedirect(reverse('zapp:registration_login'))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('zapp:registration_login') + '?logout')


def sitrep(request):
    todo_listing = []
    for todo_list in List.objects.all():
        todo_dict = {}
        todo_dict['list_object'] = todo_list
        todo_dict['item_count'] = todo_list.item_set.count()
        todo_dict['items_complete'] = todo_list.total_completed()
        todo_dict['percent_complete'] = int(float(todo_dict['items_complete']) / todo_dict['item_count'] * 100)
        todo_listing.append(todo_dict)
    return render(request, 'zapp/sitrep.html', {'todo_listing': todo_listing})
