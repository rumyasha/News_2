from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

class Source(models.Model):
    """Источник новостей (например, Kaktus Media)"""
    name = models.CharField(max_length=200, verbose_name=_('Название'))
    url = models.URLField(verbose_name=_('URL источника'))
    is_active = models.BooleanField(default=True, verbose_name=_('Активен'))

    class Meta:
        verbose_name = _('Источник')
        verbose_name_plural = _('Источники')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Название'))
    slug = models.SlugField(unique=True, blank=True)  # Разрешаем временно пустое значение

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Article(models.Model):
    """Новостная статья"""
    title = models.CharField(max_length=500, verbose_name=_('Заголовок'))
    content = models.TextField(verbose_name=_('Содержание'))
    url = models.URLField(verbose_name=_('Ссылка на статью'))
    source = models.ForeignKey(Source, on_delete=models.CASCADE, verbose_name=_('Источник'))
    categories = models.ManyToManyField(Category, verbose_name=_('Категории'))
    published_at = models.DateTimeField(verbose_name=_('Дата публикации'))
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(blank=True, null=True, verbose_name=_('Изображение'))

    class Meta:
        verbose_name = _('Статья')
        verbose_name_plural = _('Статьи')
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at']),
        ]

    def __str__(self):
        return self.title[:50] + '...' if len(self.title) > 50 else self.title