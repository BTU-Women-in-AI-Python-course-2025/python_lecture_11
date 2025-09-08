from datetime import date
from django.db import models


class Author(models.Model):
    first_name = models.CharField(verbose_name='სახელი', max_length=100)
    last_name = models.CharField(verbose_name='გვარი', max_length=100)
    email = models.EmailField(verbose_name='მეილი')
    birth_date = models.DateField(verbose_name='დაბადების თარიღი', null=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def age(self) -> int:
        today = date.today()
        return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

    def get_blog_posts(self):
        return self.blog_posts.all()

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.first_name + " " + self.last_name


class BlogPost(models.Model):
    authors = models.ManyToManyField(
        to='blog.Author', verbose_name='ავტორები', related_name='blog_posts')

    title = models.CharField(verbose_name="სათაური", max_length=255)
    text = models.TextField(verbose_name="ტექსი")
    active = models.BooleanField(default=True, verbose_name='აქტიურია')
    create_date = models.DateTimeField(
        verbose_name="შექმნის თარიღი", auto_now_add=True, null=True)
    update_date = models.DateTimeField(
        verbose_name="განახლების თარიღი", auto_now=True, null=True)
    website = models.URLField(verbose_name='ვებ მისამართი', null=True)
    document = models.FileField(upload_to='blog_document/', null=True, blank=True)
    deleted = models.BooleanField(verbose_name='წაშლილია', default=False)
    order = models.PositiveIntegerField(default=0)

    def get_images(self):
        return BlogPostImage.objects.filter(blog_post=self.id)

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ['order']
        unique_together = [['title', 'text']]

    def __str__(self):
        return self.title


class BannerImage(models.Model):
    blog_post = models.OneToOneField(
        to='blog.BlogPost',
        related_name='banner_image',
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to='banner_image/', null=True, blank=True)

    class Meta:
        verbose_name = "Banner Image"
        verbose_name_plural = "Banner Images"

    def __str__(self):
        return f'{self.blog_post.title} - {self.id} image'


class BlogPostImage(models.Model):
    blog_post = models.ForeignKey(
        to='blog.BlogPost',
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='blog_image/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Blog Post Image"
        verbose_name_plural = "Blog Post Images"
        ordering = ['order']

    def __str__(self):
        return f'{self.blog_post.title} - {self.id} image'


class BlogPostImageDescription(models.Model):
    blog_post_image = models.ForeignKey(
        to='blog.BlogPostImage',
        on_delete=models.CASCADE,
        related_name='descriptions',
        verbose_name='Blog Post Image'
    )
    text = models.TextField(verbose_name='Text')

    class Meta:
        verbose_name = "Blog Post Image Description"
        verbose_name_plural = "Blog Post Image  Descriptions"

    def __str__(self):
        return f'{self.blog_post_image.blog_post.title} - {self.id} image'
