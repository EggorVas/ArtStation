from django.shortcuts import render
from .models import *
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import *
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout

# Фильтрация списков по POST-запросу
def filtration(Post, arts):
    sorting = Post.get("sorting")
    styleFilt = Post.get("styleFilt")
    genreFilt = Post.get("genreFilt")
    techniqueFilt = Post.get("techniqueFilt")
    if styleFilt != "None":
        arts = arts.filter(style=styleFilt)
    if genreFilt != "None":
        arts = arts.filter(genre=genreFilt)
    if techniqueFilt != "None":
        arts = arts.filter(technique=techniqueFilt)
    postFilters = [sorting, styleFilt, genreFilt, techniqueFilt]
    arts = arts.order_by(sorting)
    return arts, postFilters


# Основные функции сайта
def art_list(request):
    arts = Art.objects.all()
    postFilters = None
    if request.method == "POST":
        arts, postFilters = filtration(request.POST, arts)
    else:
        arts = arts.order_by("-published_date")

    for art in arts:
        if len(art.description) > 600:
            art.description = art.description[:600] + '...'
        art.description = art.description.split('\n')
    isowner = request.user.groups.filter(name='Owners').exists()
    admin_email = User.objects.get(pk=1).email
    return render(request, 'station/art_list.html', {'arts': arts, 'isowner': isowner, 'admin_email': admin_email,
        'sorts': Art.sortingChoices, 'styles': Art.styleChoices, 'genres': Art.genreChoices,
        'techniques': Art.techniqueChoices,'postFilters': postFilters})


def art_detail(request, pk):
    isliked = Liked_art.objects.filter(user_id=request.user.id, art_id=pk).exists()
    art = Art.objects.get(pk=pk)
    owner = User.objects.get(pk=art.owner.id)
    art.description = art.description.split('\n')
    return render(request, 'station/art_detail.html', {'art': art, 'owner': owner, 'isliked':isliked})


def art_new(request):
    if not request.user.groups.filter(name='Owners').exists():
        return redirect('art_list')
    if request.method == "POST":
        form = ArtForm(request.POST, request.FILES)
        if form.is_valid():
            art = form.save(commit=False)
            art.owner = request.user
            art.published_date = timezone.now()
            art.save()
            return redirect('art_detail', pk=art.pk)
    else:
        form = ArtForm()
    return render(request, 'station/art_edit.html', {'form': form})


def art_edit(request, pk):
    art = Art.objects.get(pk=pk)
    if request.user != art.owner:
        return redirect('art_list')
    if request.method == "POST":
        form = ArtForm(request.POST, request.FILES, instance=art)
        if form.is_valid():
            art = form.save(commit=False)
            art.save()
            return redirect('art_detail', pk=art.pk)
    else:
        form = ArtForm(instance=art)
    return render(request, 'station/art_edit.html', {'form': form})


def art_delete(request, pk):
    try:
        art = Art.objects.get(pk=pk)
    except Art.DoesNotExist:
        return redirect('art_list')
    if art.owner != request.user:
        return redirect('art_detail', pk)
    if request.method == "POST":
        if request.POST.get('confirm'):
            art.delete()
            return redirect('art_list')
        else:
            return redirect('art_detail', pk)
    return render(request, 'station/art_delete.html', {'art':art})



# Функции для авторизации
def log_in(request):
    if request.user.is_authenticated:
        return redirect('art_list')
    information = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                # the password verified for the user
                if user.is_active:
                    login(request, user)
                    return redirect('art_list')
                else:
                    information = "Данные введены корректно, но профиль отключен!"
            else:
                # the authentication system was unable to verify the username and password
                information = "Логин и пароль введены некорректно."
            return render(request, 'station/login.html', {'form': form, 'info': information})
    else:
        form = LoginForm()
    return render(request, 'station/login.html', {'form': form})


def registration(request):
    if request.user.is_authenticated:
        return redirect('art_list')
    if request.method == "POST":
        form = RegForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            pw = user.password
            user.set_password(pw)
            user.save()
            user = authenticate(username=user.username, password=pw)
            login(request, user)
            return redirect('art_list')
    else:
        form = RegForm()
    return render(request, 'station/registration.html', {'form': form})


def log_out(request):
    if not request.user.is_authenticated:
        return redirect('art_list')
    logout(request)
    return redirect('art_list')


# Функции для избранного
def new_art_favorite(request, pk):
    if not request.user.is_authenticated:
        return redirect('art_list')
    art, created = Liked_art.objects.get_or_create(art_id=Art.objects.get(pk=pk), user_id=request.user)
    if created:
        art.save()
    else:
        art.delete()
    return redirect('art_detail', pk)


def art_favorites(request):
    if not request.user.is_authenticated:
        return redirect('art_list')
    likes = Liked_art.objects.filter(user_id=request.user.id)

    ids = []
    for like in likes:
        ids.append(like.art_id.pk)
    arts = Art.objects.filter(id__in=ids).order_by("-published_date")

    postFilters = None
    if request.method == "POST":
        arts, postFilters = filtration(request.POST, arts)

    for art in arts:
        if len(art.description) > 600:
            art.description = art.description[:600] + '...'
        art.description = art.description.split('\n')
    return render(request, 'station/art_list.html', {'arts': arts,
        'sorts': Art.sortingChoices, 'styles': Art.styleChoices, 'genres': Art.genreChoices,
        'techniques': Art.techniqueChoices,'postFilters': postFilters})
