# Soft Delete

This package is used for implementing soft delete functionality in models,
when used you can delete and restore deleted items unless it was hard deleted from the database.


## Installation

```
pip install dj-soft-delete
```

## Usage

you can use it by extending `HasSoftDelete` class in your model

```
    from django_soft_delete.models import HasSoftDelete
    
    
    class Item(HasSoftDelete):
        ...
```

* **retrieving items without deleted**
```
    Item.objects.all()
```

* **retrieving items with deleted**
```
    Item.with_trashed_objects.all()
```

* **retrieving deleted items only
```
    Item.with_trashed_objects.deleted()
```
* **Soft deleting item**
```
    # via objects manager
    Item.objects.filter(...).delete()

    # via model instance
    item = Item.objects.get(...)
    item.delete()
```
* **herd deleting items**
```
    # via objects manager
    Item.objects.filter(...).hard_delete()

    # via model instance
    item = Item.objects.get(...)
    item.hard_delete()
```

* **Restore soft deleted items**

```
    # via objects manager
    Item.with_trashed_objects.filter(...).restore()
    
    # via model instance
    item = Item.with_trashed_objects.get(...)
    item.restore()
```