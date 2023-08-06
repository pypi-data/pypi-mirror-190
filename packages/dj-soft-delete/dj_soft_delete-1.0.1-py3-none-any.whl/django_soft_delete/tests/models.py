from django.db import models
from django.utils.timezone import now

from django_soft_delete.models import HasSoftDelete


class TestModel(HasSoftDelete):
    title = models.CharField(blank=True, null=True, max_length=120)


class RelatedTestModel(HasSoftDelete):
    title = models.CharField(blank=True, null=True, max_length=120)
    test_model = models.ForeignKey(TestModel, on_delete=models.CASCADE)
