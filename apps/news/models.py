from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Название'))

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

    def __str__(self):
        return self.name


class Source(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Название источника'))
    url = models.URLField(verbose_name=_('URL источника'))
    parsing_interval = models.PositiveIntegerField(
        default=60,
        verbose_name=_('Интервал парсинга (минуты)')
    )
    categories = models.ManyToManyField(Category, verbose_name=_('Категории'))
    is_active = models.BooleanField(default=True, verbose_name=_('Активен'))

    class Meta:
        verbose_name = _('Источник')
        verbose_name_plural = _('Источники')

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=500, verbose_name=_('Заголовок'))
    content = models.TextField(verbose_name=_('Содержание'))
    url = models.URLField(verbose_name=_('Ссылка на статью'))
    source = models.ForeignKey(Source, on_delete=models.CASCADE, verbose_name=_('Источник'))
    categories = models.ManyToManyField(Category, verbose_name=_('Категории'))
    published_at = models.DateTimeField(verbose_name=_('Дата публикации'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    image_url = models.URLField(blank=True, null=True, verbose_name=_('Ссылка на изображение'))

    class Meta:
        verbose_name = _('Статья')
        verbose_name_plural = _('Статьи')
        ordering = ['-published_at']

    def __str__(self):
        return self.title