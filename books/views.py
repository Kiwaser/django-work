from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg

from .models import Book
from .forms import BookForm, ReviewForm


def home(request):
    """Промо-страница, доступна всем."""
    return render(request, 'home.html')


def register(request):
    """Регистрация нового пользователя."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def dashboard(request):
    """
    Список книг ТЕКУЩЕГО пользователя с фильтрацией по статусу.
    Всегда фильтруем по request.user — чужие данные недоступны.
    """
    status_filter = request.GET.get('status', 'all')

    books = Book.objects.filter(user=request.user)

    if status_filter in ('want', 'reading', 'done'):
        books = books.filter(status=status_filter)

    # агрегация средней оценки по каждой книге на уровне ORM
    books = books.annotate(avg_rating=Avg('reviews__rating'))

    context = {
        'books': books,
        'status_filter': status_filter,
        'status_choices': Book.STATUS_CHOICES,
    }
    return render(request, 'dashboard.html', context)


@login_required
def book_add(request):
    """Добавление книги. Пользователь проставляется автоматически."""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user  # жёсткая привязка к текущему юзеру
            book.save()
            return redirect('dashboard')
    else:
        form = BookForm()
    return render(request, 'book_form.html', {'form': form, 'action': 'Добавить книгу'})


@login_required
def review_add(request, book_id):
    """
    Добавление рецензии к книге.
    Доступ только к СВОИМ книгам — фильтр по request.user.
    """
    book = get_object_or_404(Book, pk=book_id, user=request.user)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.save()
            return redirect('dashboard')
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'book': book,
        'reviews': book.reviews.all(),
    }
    return render(request, 'review_form.html', context)