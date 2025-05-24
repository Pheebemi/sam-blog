from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm
from .models import Post, Comment, Category, CryptoUser
from blog.form import CommentForm
import random
from datetime import datetime, timedelta
from django.http import JsonResponse
from .models import Transaction
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

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
    # Generate sample orders data
    first_names = ['Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Ethan', 'Sophia']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller']
    statuses = ['Completed', 'Pending', 'Processing']
    
    orders = []
    for i in range(10):  # Generate 10 sample orders
        amount = round(random.uniform(100, 10000), 2)
        date = datetime.now() - timedelta(days=random.randint(0, 7))
        
        orders.append({
            'id': i + 1,
            'customer': f"{random.choice(first_names)} {random.choice(last_names)}",
            'amount': f"${amount:,.2f}",
            'status': random.choice(statuses),
            'date': date.strftime('%Y-%m-%d')
        })

    context = {
        'balance': 30345.67,
        'orders': sorted(orders, key=lambda x: x['date'], reverse=True)
    }
    
    return render(request, 'dashboard/index.html', context)

@login_required
def investments_view(request):
    context = {
        'total_invested': "85,000.00",
        'active_investments': "12",
        'total_returns': "12,750.00",
        'avg_roi': "35.5",
        'investment_plans': [
            {
                'name': 'Starter Plan',
                'return_rate': "5",
                'risk_level': 'Low Risk',
                'min_investment': "100",
                'max_investment': "1000",
                'duration': "14 Days"
            },
            {
                'name': 'Growth Plan',
                'return_rate': "15",
                'risk_level': 'Low Risk',
                'min_investment': "1,000.00",
                'max_investment': "5,000.00",
                'duration': "20 Days"
            },
            {
                'name': 'Premium Plan',
                'return_rate': "40",
                'risk_level': 'Medium Risk', 
                'min_investment': "5000.00",
                'max_investment': "50,000.00",
                'duration': "25 Days"
            },
            {
                'name': 'Elite Plan',
                'return_rate': "100",
                'risk_level': 'Medium Risk',
                'min_investment': "50,000.00",
                'max_investment': "No Limit",
                'duration': "30 Days"
            },
        ],
    }
    return render(request, 'dashboard/investments.html', context)

@login_required
def submit_investment(request):
    if request.method == 'POST':
        try:
            plan_name = request.POST.get('plan_name')
            amount = request.POST.get('amount')
            payment_method = request.POST.get('payment_method')
            wallet_address = request.POST.get('wallet_address', '')
            return_rate = request.POST.get('return_rate')
            
            # Convert amount and return rate to decimal
            amount_decimal = float(amount.replace('$', '').replace(',', ''))
            return_rate_decimal = float(return_rate.replace('%', ''))
            expected_return = amount_decimal * (1 + return_rate_decimal/100)
            
            # Set completion date based on plan duration
            duration_map = {
                'Starter Plan': 14,
                'Growth Plan': 20,
                'Premium Plan': 25,
                'Elite Plan': 30
            }
            completion_date = datetime.now() + timedelta(days=duration_map.get(plan_name, 30))

            # Create transaction
            transaction = Transaction.objects.create(
                user=request.user,
                plan_name=plan_name,
                amount=amount_decimal,
                payment_method=payment_method,
                wallet_address=wallet_address,
                return_rate=return_rate_decimal,
                expected_return=expected_return,
                completion_date=completion_date,
                status='pending'
            )
            
            return JsonResponse({
                'status': 'success',
                'transaction_id': transaction.id,
                'message': 'Transaction submitted successfully'
            })
            
        except Exception as e:
            print(f"Error processing investment: {str(e)}")  # Add logging
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

@login_required
def transactions_view(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'dashboard/transactions.html', {'transactions': transactions})

@login_required
def settings_view(request):
    return render(request, 'dashboard/settings.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            names = name.split()
            request.user.first_name = names[0]
            request.user.last_name = ' '.join(names[1:]) if len(names) > 1 else ''
            request.user.save()
            messages.success(request, 'Profile updated successfully!')
        return redirect('dashboard_settings')
    return redirect('dashboard_settings')

@login_required
def update_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
        elif len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Keep user logged in
            messages.success(request, 'Password updated successfully!')
        
        return redirect('dashboard_settings')
    return redirect('dashboard_settings')

def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, "home.html")

def privacy_view(request):
    return render(request, 'privacy.html')

def terms_view(request):
    return render(request, 'terms.html')