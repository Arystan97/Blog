from __future__ import unicode_literals
from django.views import generic
from .models import Post
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostCreateForm, UserLoginForm, UserRegistrationForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/index.html'

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

def post_create(request):
	if request.method=='POST':
		form=PostCreateForm(request.POST)
		if form.is_valid():
			post=form.save(commit=False)
			post.author=request.user
			post.save()
			return redirect('PostList')
	else:
		form=PostCreateForm()
	context={'form':form}
	return render(request, 'blog/post_create.html', context)

def user_login(request):
	if request.method=='POST':
		form=UserLoginForm(request.POST)
		if form.is_valid():
			username=request.POST['username']
			password=request.POST['password']
			user=authenticate(username=username, password=password)
			if user:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(reverse('PostList'))
				else:
					return HttpResponse("User is not active")
			else:
				return HttpResponse("User is None")
	else:
		form=UserLoginForm()

	context={'form':form, }
	return render(request, 'blog/login.html', context)

def user_logout(request):
	logout(request)
	return redirect('PostList')

def register(request):
	if request.method=='POST':
		form=UserRegistrationForm(request.POST or None)
		if form.is_valid():
			new_user=form.save(commit=False)
			new_user.set_password(form.cleaned_data['password'])
			new_user.save()
			return redirect('PostList')
	else:
		form=UserRegistrationForm()
	context={'form':form, }
	return render(request, 'registration/register.html', context)

def post_detail(request, slug):
    template_name = 'blog/post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})
