# Django Admin: Inline ModelAdmin

## Introduction

Inline ModelAdmins allow you to edit related models directly on the parent model's admin page. This creates a more intuitive interface for managing related objects without navigating between different admin pages.

## Types of Inlines

Django provides two main types of inline admin classes:

1. **TabularInline**: Displays related objects in a table format (compact)
2. **StackedInline**: Displays related objects in a stacked form layout (more spacious)

## Basic Implementation

### 1. Create an Inline Class

```python
from django.contrib import admin
from .models import ParentModel, ChildModel

class ChildModelInline(admin.TabularInline):  # or admin.StackedInline
    model = ChildModel
    extra = 1  # Number of empty forms to display
```

### 2. Add to Parent ModelAdmin

```python
@admin.register(ParentModel)
class ParentModelAdmin(admin.ModelAdmin):
    inlines = [ChildModelInline]
```

## Common Inline Options

| Option | Description | Example |
|--------|-------------|---------|
| `model` | The related model to inline | `model = Comment` |
| `extra` | Number of empty forms to display | `extra = 3` |
| `max_num` | Maximum number of forms to display | `max_num = 10` |
| `min_num` | Minimum number of forms to display | `min_num = 1` |
| `classes` | CSS classes to apply to the inline | `classes = ['collapse']` |
| `fields` | Fields to include (same as ModelAdmin) | `fields = ('name', 'email')` |
| `readonly_fields` | Fields that are read-only | `readonly_fields = ('created_at',)` |
| `raw_id_fields` | Display FK/M2M as raw ID instead of dropdown | `raw_id_fields = ('user',)` |

## Example: Complete Implementation

```python
from django.contrib import admin
from .models import Author, Book

class BookInline(admin.TabularInline):
    model = Book
    extra = 1
    fields = ('title', 'isbn', 'publication_date')
    readonly_fields = ('created_at',)
    classes = ['collapse']
    
    # Optional: limit choices for foreign keys
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "publisher":
            kwargs["queryset"] = Publisher.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookInline]
    list_display = ('name', 'email', 'total_books')
    
    def total_books(self, obj):
        return obj.books.count()
    total_books.short_description = 'Books Published'
```

## Advanced Techniques

### 1. Conditional Inlines

```python
class ConditionalInline(admin.TabularInline):
    def get_extra(self, request, obj=None, **kwargs):
        if obj and obj.special_condition:
            return 0
        return 2
```

### 2. Dynamic Fields

```python
class DynamicFieldsInline(admin.TabularInline):
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not request.user.is_superuser:
            fields.remove('sensitive_field')
        return fields
```

### 3. Inline for ManyToMany (through model)

```python
class MembershipInline(admin.TabularInline):
    model = Group.members.through  # For M2M through model
    extra = 1
```

## Nested Inlines (django-nested-admin)

For nested inlines (inlines within inlines), you'll need the `django-nested-admin` package:

```python
# Requires installation of django-nested-admin
# Install with: pip install django-nested-admin
from nested_admin import NestedTabularInline, NestedModelAdmin

class ChapterInline(NestedTabularInline):
    model = Chapter
    extra = 1

class BookInline(NestedTabularInline):
    model = Book
    inlines = [ChapterInline]
    extra = 1

@admin.register(Author)
class AuthorAdmin(NestedModelAdmin):
    inlines = [BookInline]
```

### Installation Instructions:

1. Install the package:
```bash
pip install django-nested-admin
```

2. Add to your INSTALLED_APPS:
```python
INSTALLED_APPS = [
    ...
    'nested_admin',
    ...
]
```

3. Include the URLs in your urls.py:
```python
from django.urls import path, include

urlpatterns = [
    ...
    path('_nested_admin/', include('nested_admin.urls')),
    ...
]
```

## Best Practices

1. Use `TabularInline` for simple relationships with few fields
2. Use `StackedInline` for complex relationships or models with many fields
3. Set reasonable values for `extra` (typically 1-3)
4. Consider using `classes = ['collapse']` for less frequently used inlines
5. For performance with large datasets, consider `raw_id_fields`
6. Override `get_queryset()` to control which related objects are displayed
