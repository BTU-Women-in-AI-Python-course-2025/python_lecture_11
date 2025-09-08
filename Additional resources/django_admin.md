# Django Admin: Registering Models

## Introduction

Django's admin interface is one of its most powerful features, providing a ready-to-use UI for managing your application's data.
To make your models accessible through the admin interface, you need to register them.

---

## Registering Models with Django Admin

### Basic Registration

To make a model accessible in the admin interface, you need to:

1. Import the model
2. Register it using `admin.site.register()`

```python
from django.contrib import admin
from .models import YourModel

admin.site.register(YourModel)
```

---

### Customizing ModelAdmin

You can customize how your model appears in the admin interface by creating a `ModelAdmin` class:

```python
from django.contrib import admin
from .models import YourModel

class YourModelAdmin(admin.ModelAdmin):
    list_display = ('field1', 'field2', 'field3')  # Fields to display in list view
    list_filter = ('field1', 'field2')             # Fields to filter by
    search_fields = ('field1', 'field2')           # Fields to search in
    ordering = ('-field1',)                        # Default ordering

admin.site.register(YourModel, YourModelAdmin)
```

---

### Common ModelAdmin Options

| Option                | Description                                  | Example                           |
| --------------------- | -------------------------------------------- | --------------------------------- |
| `list_display`        | Fields to display in the list view           | `('name', 'email', 'created_at')` |
| `list_filter`         | Fields to enable filtering by                | `('is_active', 'category')`       |
| `search_fields`       | Fields to enable search functionality        | `('title', 'description')`        |
| `ordering`            | Default ordering of records                  | `('-created_at',)`                |
| `readonly_fields`     | Fields that are displayed but not editable   | `('created_at', 'updated_at')`    |
| `list_per_page`       | Number of items per page                     | `50`                              |
| `date_hierarchy`      | Enable date-based navigation                 | `'created_at'`                    |
| `fields`              | Control which fields are displayed and order | `('title', 'content', 'author')`  |
| `exclude`             | Fields to exclude from the form              | `('secret_field',)`               |
| `filter_horizontal`   | Dual horizontal selector for ManyToMany      | `('tags',)`                       |
| `filter_vertical`     | Dual vertical selector for ManyToMany        | `('tags',)`                       |
| `fieldsets`           | Group fields into sections with options      | See `Using Fieldsets` below       |
| `prepopulated_fields` | Auto-fill fields (client-side)               | `{'slug': ('title',)}`            |

---

### Using Fieldsets

The `fieldsets` option allows you to organize fields into **sections** on the edit page. Each fieldset is a tuple: `(title, {"fields": (...)})`.

#### Example

```python
class ArticleAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Basic Information", {
            "fields": ("title", "slug", "author")
        }),
        ("Content", {
            "fields": ("content", "tags"),
        }),
        ("Publication Settings", {
            "fields": ("is_published", "published_date"),
        }),
    )
```

---

### Using `prepopulated_fields`

`prepopulated_fields` is a convenient admin-only, client-side feature that pre-fills a field (typically a slug) from one or more source fields. It is implemented with admin JavaScript and affects only the admin UI.

#### Basic usage

```python
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
```

* Key is the target field (usually a `SlugField` or `CharField`).
* Value is a tuple of one or more source fields whose values will be joined and slugified in the UI.

#### Multiple source fields

You can use multiple source fields; their values are concatenated and slugified:

```python
prepopulated_fields = {'slug': ('first_name', 'last_name')}
```

#### Important notes & best practices

* This is **client-side only** (JavaScript in admin). The browser generates the slug while the user types — it does **not** guarantee the model field will always be populated outside the admin.
* Ensure the source fields are present in the form (in your `fields` or `fieldsets`) — otherwise the admin JS can't read them.
* If you need server-side guarantees (e.g., automatic slug on save, uniqueness), implement slug generation in the model's `save()` or in `save_model()` on the admin side:

```python
# models.py
from django.utils.text import slugify

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)  # allow blank so admin can prepopulate

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
```

* If you want admin to overwrite an existing slug when sources are changed, you must handle that server-side (or clear the slug field manually in the admin form).
* Use `prepopulated_fields` mainly as a UX helper for the admin; don't rely on it for data integrity.

---

### Many-to-Many Field Interfaces

By default, Django displays a **multi-select box** for `ManyToManyField`. You can change this representation in the admin:

#### 1. Default (Multi-Select Box)

```python
class BookAdmin(admin.ModelAdmin):
    pass
```

#### 2. Horizontal Filter

```python
class BookAdmin(admin.ModelAdmin):
    filter_horizontal = ('authors',)
```

#### 3. Vertical Filter

```python
class BookAdmin(admin.ModelAdmin):
    filter_vertical = ('authors',)
```

#### 4. Inline Editing (with Through Model)

If you have a custom `through` model, you can manage it inline:

```python
class BookAuthorInline(admin.TabularInline):  # or admin.StackedInline
    model = Book.authors.through
    extra = 1

class BookAdmin(admin.ModelAdmin):
    inlines = [BookAuthorInline]
    exclude = ('authors',)  # Hide the default widget
```

---

### Inline Models

For related models, you can use inlines to edit them on the parent model's page:

```python
class RelatedModelInline(admin.TabularInline):  # or admin.StackedInline
    model = RelatedModel
    extra = 1  # Number of empty forms to display

class YourModelAdmin(admin.ModelAdmin):
    inlines = [RelatedModelInline]
```

---

### Decorator Syntax (Alternative Registration)

You can also use the `@admin.register` decorator:

```python
from django.contrib import admin
from .models import YourModel

@admin.register(YourModel)
class YourModelAdmin(admin.ModelAdmin):
    list_display = ('field1', 'field2')
    # other configurations...
```

---

## Best Practices

1. Always create custom `ModelAdmin` classes for important models.
2. Use `prepopulated_fields` for slug fields to improve admin UX, but also generate slugs server-side for data integrity.
3. Consider user permissions when designing admin interfaces.
4. Override `save_model()` for custom save behavior when necessary.
5. Use `get_queryset()` to control which objects are visible to different users.
6. Use `filter_horizontal` / `filter_vertical` for ManyToMany fields with large datasets.
7. Use inlines when working with custom `through` models.
8. Use `fieldsets` to organize complex forms into clear sections.

---

## Example: Complete ModelAdmin Configuration

```python
from django.contrib import admin
from .models import Article, Author

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')
    fieldsets = (
        (None, {
            "fields": ("name", "email"),
        }),
        ("Additional Information", {
            "fields": ("bio", "website"),
        }),
    )
    
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'is_published')
    list_filter = ('is_published', 'published_date')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}   # <-- prepopulated_fields example
    raw_id_fields = ('author',)
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)
    filter_horizontal = ('tags',)  # Example for ManyToMany field

    fieldsets = (
        ("Basic Information", {
            "fields": ("title", "slug", "author")
        }),
        ("Content", {
            "fields": ("content", "tags"),
        }),
        ("Publication Settings", {
            "fields": ("is_published", "published_date"),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_published=True)

admin.site.register(Author, AuthorAdmin)
admin.site.register(Article, ArticleAdmin)
```
