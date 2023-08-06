import datetime
import inspect

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.test import TestCase
from django.utils.translation import gettext as _

from .models import TestModel, RelatedTestModel
from ..models import HasSoftDelete, SoftDeleteManager, SoftDeleteQueryset


class HasSoftDeleteStructureTestCase(TestCase):
    def test_it_extends_django_model(self):
        self.assertTrue(issubclass(HasSoftDelete, models.Model))

    def test_its_class_meta_verbose_name(self):
        self.assertTrue(HasSoftDelete._meta.abstract)

    def test_it_has_deleted_at_field(self):
        self.assertIsNotNone(HasSoftDelete._meta.get_field('deleted_at'))

    def test_deleted_at_field_is_instance_of_DateTimeField(self):
        field = HasSoftDelete._meta.get_field('deleted_at')
        self.assertIsInstance(field, models.DateTimeField)

    def test_deleted_at_field_verbose_name_is_deleted_at(self):
        field = HasSoftDelete._meta.get_field('deleted_at')
        self.assertEquals(field.verbose_name, _('Deleted At'))

    def test_deleted_at_field_default_value_is_none(self):
        field = HasSoftDelete._meta.get_field('deleted_at')
        self.assertEquals(field.default, None)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_it_has_hard_delete_method(self):
        self.assertTrue(hasattr(HasSoftDelete, 'hard_delete'))
        self.assertTrue(callable(HasSoftDelete.hard_delete))

    def test_hard_delete_signature(self):
        expected_signature = ['self']
        actual_signature = inspect.getfullargspec(HasSoftDelete.hard_delete)[0]
        self.assertEquals(actual_signature, expected_signature)

    def test_it_has_restore_method(self):
        self.assertTrue(hasattr(HasSoftDelete, 'restore'))
        self.assertTrue(callable(HasSoftDelete.restore))

    def test_restore_signature(self):
        expected_signature = ['self']
        actual_signature = inspect.getfullargspec(HasSoftDelete.restore)[0]
        self.assertEquals(actual_signature, expected_signature)


class HasSoftDeleteDeleteTestCase(TestCase):
    def setUp(self):
        self.obj = TestModel.objects.create(title='new model')

    def test_it_raises_ObjectDoesNotExist_if_object_was_soft_deleted(self):
        self.obj.delete()
        with self.assertRaises(ObjectDoesNotExist) as e:
            self.obj.delete()
            self.assertEquals(e.exception, "This object was deleted before!")

    def test_it_updates_object_instance_deleted_at_to_now(self):
        self.obj.delete()
        self.obj.refresh_from_db()
        self.assertIsNotNone(self.obj.deleted_at)
        self.assertIsInstance(self.obj.deleted_at, datetime.datetime)


class HasSoftDeleteRestoreTestCase(TestCase):
    def setUp(self):
        self.obj = TestModel.objects.create(title='new model')
        self.obj.delete()
        self.obj.refresh_from_db()

    def test_it_updates_object_instance_deleted_at_to_now(self):
        self.obj.restore()
        self.obj.refresh_from_db()
        self.assertIsNone(self.obj.deleted_at)


class HasSoftDeleteHardDeleteTestCase(TestCase):
    def setUp(self):
        self.obj = TestModel.objects.create(title='new model')

    def test_it_deletes_object_entirely(self):
        self.obj.hard_delete()
        self.assertEquals(TestModel.objects.count(), 0)


class SoftDeleteManagerStructureTestCase(TestCase):
    def test__init__signature(self):
        expected_signature = ['self', 'with_trashed']
        actual_signature = inspect.getfullargspec(SoftDeleteManager.__init__)[0]
        self.assertEquals(actual_signature, expected_signature)

    def test_it_has_get_queryset_method(self):
        self.assertTrue(hasattr(SoftDeleteManager, 'get_queryset'))
        self.assertTrue(callable(SoftDeleteManager.get_queryset))

    def test_get_queryset_signature(self):
        expected_signature = ['self']
        actual_signature = inspect.getfullargspec(SoftDeleteManager.get_queryset)[0]
        self.assertEquals(actual_signature, expected_signature)


class SoftDeleteManagerTestCase(TestCase):
    def setUp(self):
        for i in range(6):
            test_model = TestModel.objects.create(title=str(i))
            for j in range(2):
                test_model.relatedtestmodel_set.create(title=str(j))

    def test_it_soft_deletes_related_models_through_manager(self):
        test_model = TestModel.objects.get(pk=1)
        test_model.relatedtestmodel_set.filter(pk=1).delete()
        related_test_model = RelatedTestModel.with_trashed_objects.filter(pk=1)
        self.assertTrue(related_test_model.exists())
        self.assertIsNotNone(related_test_model.first().deleted_at)

    def test_it_hard_deletes_related_models_through_manager(self):
        test_model = TestModel.objects.get(pk=1)
        test_model.relatedtestmodel_set.filter(pk=1).hard_delete()
        related_test_model = RelatedTestModel.with_trashed_objects.filter(pk=1)
        self.assertFalse(related_test_model.exists())


class SoftDeleteQuerysetStructureTestCase(TestCase):
    def test_it_has_delete_method(self):
        self.assertTrue(hasattr(SoftDeleteQueryset, 'delete'))
        self.assertTrue(callable(SoftDeleteQueryset.delete))

    def test_delete_signature(self):
        expected_signature = ['self']
        actual_signature = inspect.getfullargspec(SoftDeleteQueryset.delete)[0]
        self.assertEquals(actual_signature, expected_signature)

    def test_it_has_hard_delete_method(self):
        self.assertTrue(hasattr(SoftDeleteQueryset, 'hard_delete'))
        self.assertTrue(callable(SoftDeleteQueryset.hard_delete))

    def test_hard_delete_signature(self):
        expected_signature = ['self']
        actual_signature = inspect.getfullargspec(SoftDeleteQueryset.hard_delete)[0]
        self.assertEquals(actual_signature, expected_signature)

    def test_it_has_restore_method(self):
        self.assertTrue(hasattr(SoftDeleteQueryset, 'restore'))
        self.assertTrue(callable(SoftDeleteQueryset.restore))

    def test_restore_signature(self):
        expected_signature = ['self']
        actual_signature = inspect.getfullargspec(SoftDeleteQueryset.restore)[0]
        self.assertEquals(actual_signature, expected_signature)

    def test_it_has_deleted_method(self):
        self.assertTrue(hasattr(SoftDeleteQueryset, 'deleted'))
        self.assertTrue(callable(SoftDeleteQueryset.deleted))

    def test_deleted_signature(self):
        expected_signature = ['self']
        actual_signature = inspect.getfullargspec(SoftDeleteQueryset.deleted)[0]
        self.assertEquals(actual_signature, expected_signature)


class SoftDeleteQuerysetDeleteTestCase(TestCase):
    def test_it_sets_deleted_at_to_now(self):
        for i in range(6):
            TestModel.objects.create(title=str(i))

        TestModel.objects.filter(pk__in=[1, 2, 3]).delete()

        self.assertTrue(
            all(obj.deleted_at is not None for obj in TestModel.with_trashed_objects.filter(pk__in=[1, 2, 3])))


class SoftDeleteQuerysetHardDeleteTestCase(TestCase):
    def test_it_deletes_objects_completely(self):
        for i in range(6):
            TestModel.objects.create(title=str(i))

        TestModel.objects.filter(pk__in=[1, 2, 3]).hard_delete()

        self.assertFalse(TestModel.with_trashed_objects.filter(pk__in=[1, 2, 3]).exists())


class SoftDeleteQuerysetRestoreTestCase(TestCase):
    def test_it_restores_soft_deleted_objects(self):
        for i in range(6):
            TestModel.objects.create(title=str(i))

        TestModel.objects.filter(pk__in=[1, 2, 3]).delete()

        TestModel.with_trashed_objects.filter(pk__in=[1, 2, 3]).restore()

        self.assertTrue(TestModel.objects.filter(pk__in=[1, 2, 3]).exists())


class SoftDeleteQuerysetDeletedTestCase(TestCase):
    def test_it_restores_soft_deleted_objects(self):
        for i in range(6):
            TestModel.objects.create(title=str(i))

        TestModel.objects.filter(pk__in=[1, 2, 3]).delete()

        self.assertEquals(
            list(TestModel.with_trashed_objects.filter(deleted_at__isnull=False)),
            list(TestModel.with_trashed_objects.deleted()))
