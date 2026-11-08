from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from core.models import TimeStampedUUIDModel
from core.validators import validate_file_safety


class NewsCategory(TimeStampedUUIDModel):
    """
    Category for institutional News articles (news_categories).
    """
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = 'news_categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class NewsArticle(TimeStampedUUIDModel):
    """
    Institutional News article published by PLUS (news_articles).
    """

    class PublicationStatus(models.TextChoices):
        DRAFT = 'DRAFT', 'Borrador'
        PUBLISHED = 'PUBLISHED', 'Publicada'
        ARCHIVED = 'ARCHIVED', 'Archivada'

    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True, blank=True)
    summary = models.TextField()
    content = models.TextField()
    cover_image = models.FileField(
        upload_to='news/covers/%Y/%m/',
        null=True,
        blank=True,
        validators=[validate_file_safety],
    )
    category = models.ForeignKey(
        NewsCategory,
        on_delete=models.PROTECT,
        related_name='articles',
    )
    related_initiative = models.ForeignKey(
        'initiatives.Initiative',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='news_articles',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='authored_news',
    )
    publication_status = models.CharField(
        max_length=15,
        choices=PublicationStatus.choices,
        default=PublicationStatus.DRAFT,
        db_index=True,
    )
    is_featured = models.BooleanField(default=False, db_index=True)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        db_table = 'news_articles'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(
                fields=['publication_status', '-published_at'],
                name='idx_news_pub_date',
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while NewsArticle.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        if self.publication_status == self.PublicationStatus.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
