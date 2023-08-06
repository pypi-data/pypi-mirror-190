from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext as _


class SoftDeleteQueryset(models.QuerySet):
    def delete(self):
        return self.update(deleted_at=now())

    def hard_delete(self):
        return super().delete()

    def restore(self):
        return self.update(deleted_at=None)

    def deleted(self):
        return self.filter(deleted_at__isnull=False)


class SoftDeleteManager(models.Manager):
    def __init__(self, with_trashed=False, *args, **kwargs):
        self.with_trashed = with_trashed
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        qs = SoftDeleteQueryset(self.model, using=self._db)
        return qs if self.with_trashed else qs.filter(deleted_at__isnull=True)

    def deleted(self):
        return self.get_queryset().deleted()


class HasSoftDelete(models.Model):
    class Meta:
        abstract = True

    objects = SoftDeleteManager()
    with_trashed_objects = SoftDeleteManager(with_trashed=True)

    deleted_at = models.DateTimeField(blank=True, null=True, default=None, verbose_name=_('Deleted At'))

    def delete(self, *args, **kwargs):
        if self.deleted_at:
            raise ObjectDoesNotExist(_("This object was deleted before!"))
        self.deleted_at = now()
        self.save()

    def hard_delete(self):
        return super(HasSoftDelete, self).delete()

    def restore(self):
        self.deleted_at = None
        self.save()
