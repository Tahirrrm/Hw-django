from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.contrib.auth import authenticate, login as auth_login

# База данных пользователей
USERS_DB = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'user1': {'password': 'user123', 'role': 'user'},
    'user2': {'password': 'user456', 'role': 'user'}
}

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Проверка пользователя
            user = USERS_DB.get(username)
            if user and user['password'] == password:
                request.session['role'] = user['role']
                request.session['username'] = username
                return redirect('welcome')
            else:
                messages.error(request, 'Неверный логин или пароль')
    else:
        form = LoginForm()
    
    return render(request, 'web_form/login.html', {'form': form})

def welcome_view(request):
    role = request.session.get('role')
    username = request.session.get('username')
    
    if role and username:
        return render(request, 'web_form/welcome.html', {
            'username': username,
            'role': role
        })
    else:
        return redirect('login')

def logout_view(request):
    request.session.flush()
    return redirect('login')