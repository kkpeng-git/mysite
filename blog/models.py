from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse

from read_statistics.models import ReadNumExpandMethod, ReadDetaill


class BlogType(models.Model):
    """ 博客类型 """
    type_name = models.CharField(max_length=20, verbose_name="博客类型")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    def __str__(self):
        return self.type_name


class Blog(models.Model, ReadNumExpandMethod):
    """ 博客 """
    title = models.CharField(max_length=50, verbose_name="标题")
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE, verbose_name="博客类型")
    # content = models.TextField()
    content = RichTextUploadingField(verbose_name="正文")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    read_details = GenericRelation(ReadDetaill)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    last_updated_time = models.DateTimeField(auto_now=True, verbose_name="最后修改")

    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_pk': self.pk})

    def get_email(self):
        return self.author.email

    def __str__(self):
        return "<Blog:%s>" % self.title

    class Meta:
        ordering = ["-created_time"]  # 根据创建时间进行排序
