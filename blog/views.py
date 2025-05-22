from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm
from .models import Post, Comment, Category, CryptoUser
from blog.form import CommentForm

def blog_index(request):
    context = {
        'posts': Post.objects.all().order_by('-created_on')
    }
    return render(request, "blog_index.html", context)

def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by("-created_on")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)

def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)
    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        'form' : CommentForm(),
    }
    return render(request, "blog/detail.html", context)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'registration/login.html', {
                'error': 'Invalid username or password'
            })
    return render(request, 'registration/login.html')

@login_required
def dashboard_view(request):
    return render(request, 'dashboard/index.html')

@login_required
def investments_view(request):
    return render(request, 'dashboard/investments.html')

@login_required
def transactions_view(request):
    return render(request, 'dashboard/transactions.html')

@login_required
def settings_view(request):
    return render(request, 'dashboard/settings.html')
def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, "home.html")