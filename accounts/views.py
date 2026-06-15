from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import RegisterForm, LoginForm, UsernameForm, EmailForm, ProfilePasswordChangeForm, AvatarForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('datasets:list')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'Bienvenue {user.username} !')
        return redirect('datasets:list')
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('datasets:list')
    form = LoginForm(request, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f'Bienvenue {user.username} !')
        return redirect(request.GET.get('next', 'datasets:list'))
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Vous avez été déconnecté.')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)
    action = request.POST.get('action') if request.method == 'POST' else None

    username_form = UsernameForm(
        request.POST if action == 'username' else None,
        instance=user
    )
    email_form = EmailForm(
        request.POST if action == 'email' else None,
        instance=user
    )
    password_form = ProfilePasswordChangeForm(
        user,
        request.POST if action == 'password' else None
    )
    avatar_form = AvatarForm(
        request.POST if action == 'avatar' else None,
        request.FILES if action == 'avatar' else None,
        instance=profile
    )

    if action == 'username' and username_form.is_valid():
        username_form.save()
        messages.success(request, "Nom d'utilisateur mis à jour.")
        return redirect('accounts:profile')

    if action == 'email' and email_form.is_valid():
        email_form.save()
        messages.success(request, 'Adresse e-mail mise à jour.')
        return redirect('accounts:profile')

    if action == 'password' and password_form.is_valid():
        password_form.save()
        update_session_auth_hash(request, password_form.user)
        messages.success(request, 'Mot de passe modifié avec succès.')
        return redirect('accounts:profile')

    if action == 'avatar' and avatar_form.is_valid():
        avatar_form.save()
        messages.success(request, 'Photo de profil mise à jour.')
        return redirect('accounts:profile')

    if action == 'remove_avatar':
        if profile.avatar:
            profile.avatar.delete(save=True)
        messages.success(request, 'Photo de profil supprimée.')
        return redirect('accounts:profile')

    return render(request, 'accounts/profile.html', {
        'username_form': username_form,
        'email_form': email_form,
        'password_form': password_form,
        'avatar_form': avatar_form,
        'profile': profile,
    })
