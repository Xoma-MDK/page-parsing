# myapp/models.py
from django.db import models
class Article(models.Model):
    title = models.CharField(max_length=300, verbose_name="Заголовок")
    url = models.URLField(verbose_name="Ссылка на статью", unique=True)
    published = models.DateTimeField(verbose_name="Дата публикации")
    source = models.CharField(max_length=50, default="lenta", verbose_name="Источник")
    text = models.TextField(blank=True, null=True, verbose_name="Текст статьи (превью)") # pyright: ignore[reportUndefinedVariable]

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-published"]

    def __str__(self):
        return f"{self.title} ({self.source})"
    
    def get_short_title(self):
        """Сокращенный заголовок для отображения"""
        if len(self.title) > 50:
            return self.title[:47] + '...'
        return self.title