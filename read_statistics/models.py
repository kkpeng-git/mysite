from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from django.utils import timezone


class ReadNum(models.Model):
    """ 阅读量 """
    read_num = models.IntegerField(default=0, verbose_name="阅读计数")

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class ReadNumExpandMethod():
    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0


class ReadDetaill(models.Model):
    """ 统计每天的阅读量 """
    date = models.DateField(default=timezone.now, verbose_name="时间")
    read_num = models.IntegerField(default=0, verbose_name="阅读计数")

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
