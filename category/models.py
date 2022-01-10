from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, db_index=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse("products_by_category", kwargs={"category_slug": self.slug})

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs): 
        self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)
    