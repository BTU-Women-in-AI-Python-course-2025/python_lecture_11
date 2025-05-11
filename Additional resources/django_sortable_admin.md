# Django Admin: Sortable Models and Inlines

## Introduction

Django's admin interface doesn't natively support drag-and-drop sorting of models, but we can easily add this functionality using the `django-admin-sortable2` package. This is particularly useful for models that need manual ordering (like featured items, menu items, etc.).

## Installation

First, install the package:

```bash
pip install django-admin-sortable2
```

Add to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'adminsortable2',
    ...
]
```

## Basic Implementation

### 1. Add Sortable Field to Model

First, add an ordering field to your model:

```python
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    
    class Meta:
        ordering = ['order']  # Important for correct initial ordering
```

### 2. Make Model Admin Sortable

```python
from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import Category

@admin.register(Category)
class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'order')
```

## Sortable Inlines

For sortable nested inlines:

```python
from adminsortable2.admin import SortableInlineAdminMixin

class ItemInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Item
    extra = 1
    ordering = ['order']  # Requires an 'order' field on the Item model
```

## Advanced Configuration

### Customizing the Sort Field

If you want to use a different field name than `order`:

```python
class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    sortable_by = 'position'  # Use this if your field is named 'position'
```

### Changing Display Order

Control how items are initially displayed:

```python
class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    ordering = ['-order']  # Reverse order
```

### Disabling Sorting for Specific Users

```python
class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    def get_ordering(self, request):
        if not request.user.is_superuser:
            return ['name']  # Non-superusers see alphabetical order
        return super().get_ordering(request)
```

## Common Patterns

### 1. Sortable with Parent Relationship

```python
class MenuItem(models.Model):
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0, db_index=True)
    
    class Meta:
        ordering = ['menu', 'order']

@admin.register(MenuItem)
class MenuItemAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'menu', 'order')
    list_filter = ('menu',)
```

### 2. Sortable Stacked Inlines

```python
class ChapterAdmin(SortableInlineAdminMixin, admin.StackedInline):
    model = Chapter
    extra = 1
    ordering = ['order']
```

## Best Practices

1. Always add `db_index=True` to your ordering field for better performance
2. Include the ordering field in your model's `Meta` class
3. For large datasets, consider adding `ordering = ['order']` to the model's Meta class
4. Use consistent ordering fields across related models
5. Test sorting with different user permission levels

## Troubleshooting

**Issue:** Sorting doesn't work
- Solution: Make sure:
  - The package is in INSTALLED_APPS
  - You have an ordering field in your model
  - The field is included in the model's Meta ordering
  - JavaScript is loading (check browser console)

**Issue:** Items jump back after sorting
- Solution: Clear your browser cache or check for conflicting JavaScript
