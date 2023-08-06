"""
Copyright (c) 2014-present, aglean Inc.
"""
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .utils import image_path, image_url


class Tag(models.Model):
    # detail
    name = models.CharField(_('Name'), max_length=255, unique=True)
    image = models.ImageField(
        _('Cover image'),
        upload_to=image_path,
        help_text=_(
            'Upload file should under size limitation, '
            'with png, jpg or jpeg file extensions.'
        ),
        blank=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        return image_url(self)

    @property
    def article_count(self):
        return self.article_set.filter(is_published=True).count()


class Category(models.Model):
    # relationship
    tags = models.ManyToManyField(Tag, verbose_name=_('Tags'))

    # detail
    name = models.CharField(_('Name'), max_length=255, unique=True)
    description = models.TextField(_('Description'), blank=True)
    image = models.ImageField(
        _('Cover image'),
        upload_to=image_path,
        help_text=_(
            'Upload file should under size limitation, '
            'with png, jpg or jpeg file extensions.'
        ),
        blank=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        return image_url(self)

    @property
    def tag_count(self):
        return self.tags.count()


class Article(models.Model):
    # relationship
    tags = models.ManyToManyField(Tag, verbose_name=_('Tags'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.SET_NULL,
                               null=True,
                               verbose_name=_('Author'))

    # detail
    title = models.CharField(_('Title'), max_length=255)
    slug = models.SlugField(
        _('Slug'),
        help_text=_(
            'Characters combine with numbers, underscores or hyphens.'
            'Ex: today1_news-headline'
        ),
        allow_unicode=True,
        blank=True
    )
    summary = models.TextField(_('Summary'))
    image = models.ImageField(
        _('Cover image'),
        upload_to=image_path,
        help_text=_(
            'Upload file should under size limitation, '
            'with png, jpg or jpeg file extensions.'
        ),
        blank=True
    )

    # flag
    is_published = models.BooleanField(
        _('Publish'),
        help_text=_('Designates whether the item is published on the site.'),
        default=True
    )

    # datetime
    published_at = models.DateTimeField(_('Published at'),
                                        blank=True,
                                        null=True)
    created_at = models.DateTimeField(_('Created at'),
                                      auto_now=False,
                                      auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'),
                                      auto_now=True,
                                      auto_now_add=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        return image_url(self)


@receiver(pre_save, sender=Article)
def post_article_process(sender, instance, **kwargs):

    if instance.is_published and instance.published_at is None:
        instance.published_at = timezone.now()

    if not instance.slug.strip():
        instance.slug = slugify(instance.title, allow_unicode=True)


class Paragraph(models.Model):
    # relationship
    article = models.ForeignKey(Article,
                                on_delete=models.CASCADE,
                                verbose_name=_('Article'))

    # detail
    content = models.TextField(_('Content'), blank=True)
    image = models.ImageField(
        _('Image'),
        upload_to=image_path,
        help_text=_(
            'Upload file should under size limitation, '
            'with png, jpg or jpeg file extensions.'
        ),
        blank=True
    )
    image_text = models.CharField(
        _('Image description'),
        max_length=255,
        help_text=_('Descripe the image content'),
        blank=True
    )

    class Meta:
        ordering = ['id']
        verbose_name = _('Paragraph')
        verbose_name_plural = _('Paragraphs')

    @property
    def image_url(self):
        return image_url(self)
