from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Book(models.Model):
    STATUS_CHOICES = [
        ('want', 'Хочу прочесть'),
        ('reading', 'Читаю'),
        ('done', 'Прочитано'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name='Пользователь',
    )
    title = models.CharField(max_length=200, verbose_name='Название')
    author = models.CharField(max_length=150, verbose_name='Автор')
    genre = models.CharField(max_length=100, verbose_name='Жанр')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='want',
        verbose_name='Статус',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return f'{self.title} — {self.author}'


class Review(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Книга',
    )
    text = models.TextField(verbose_name='Текст рецензии')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оценка (1–5)',
    )
    quote = models.TextField(blank=True, verbose_name='Цитаты')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Рецензия'
        verbose_name_plural = 'Рецензии'

    def __str__(self):
        return f'Рецензия на «{self.book.title}» ({self.rating}/5)'