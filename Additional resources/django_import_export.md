# Django Import/Export: Data Management in Admin

## Introduction

The `django-import-export` package adds powerful data import/export capabilities to Django's admin interface, supporting multiple formats (XLSX, CSV, JSON, etc.). This is ideal for:
- Bulk data imports
- Data migrations
- Regular data exports
- Data sharing between systems

## Installation

```bash
pip install django-import-export
```

Add to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    ...
    'import_export',
    ...
]
```

## Basic Implementation

### 1. Create Resource Class

```python
# resources.py
from import_export import resources
from .models import Book

class BookResource(resources.ModelResource):
    class Meta:
        model = Book
        # Optional: Control which fields are included
        fields = ('id', 'title', 'author', 'published_date')
        # Optional: Exclude fields
        exclude = ('created_at',)
```

### 2. Configure ModelAdmin

```python
# admin.py
from import_export.admin import ImportExportModelAdmin
from .models import Book
from .resources import BookResource

@admin.register(Book)
class BookAdmin(ImportExportModelAdmin):
    resource_class = BookResource
    list_display = ('title', 'author', 'published_date')
```

## Key Features

### Supported Formats
- Import: XLSX, CSV, TSV, JSON, HTML, etc.
- Export: Same formats plus PDF (with reportlab)

### Field Control
```python
class BookResource(resources.ModelResource):
    full_title = fields.Field(column_name='Full Title')
    
    class Meta:
        model = Book
        fields = ('full_title', 'author__name')  # Follow relationships
        
    def dehydrate_full_title(self, book):
        return f"{book.title} ({book.published_date.year})"
```

### Import Configurations
```python
class BookAdmin(ImportExportModelAdmin):
    # Change import behavior
    import_form_class = CustomImportForm
    confirm_form_class = CustomConfirmImportForm
    
    # Export settings
    export_formats = [base_formats.XLSX, base_formats.CSV]
    
    def get_export_queryset(self, request):
        """Customize exported data"""
        return super().get_export_queryset(request).filter(active=True)
```

## Advanced Usage

### 1. Custom Field Processing
```python
class BookResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        """Pre-process row data before import"""
        row['title'] = row['title'].title()
        
    def after_import_instance(self, instance, new, **kwargs):
        """Post-process model instance"""
        if new:
            instance.created_by = kwargs['user']
```

### 2. Related Model Import
```python
class BookResource(resources.ModelResource):
    author = fields.Field(
        column_name='author',
        attribute='author',
        widget=ForeignKeyWidget(Author, 'name')
    )
    
    class Meta:
        model = Book
        fields = ('title', 'author')
```

### 3. Bulk Import with Validation
```python
def import_books(file):
    dataset = Dataset()
    dataset.load(file.read())
    result = BookResource().import_data(dataset, dry_run=True)  # Test import
    if not result.has_errors():
        BookResource().import_data(dataset, dry_run=False)  # Real import
    return result
```

## Admin Integration

### Custom Import Form
```python
from import_export.admin import ImportForm

class CustomImportForm(ImportForm):
    special_option = forms.BooleanField(required=False)

class BookAdmin(ImportExportModelAdmin):
    import_form_class = CustomImportForm
    
    def process_import(self, request, *args, **kwargs):
        form = self.get_import_form()(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['special_option']:
                # Custom import logic
                pass
        return super().process_import(request, *args, **kwargs)
```

### Export Action
```python
class BookAdmin(ImportExportModelAdmin):
    actions = ['export_selected']
    
    def export_selected(self, request, queryset):
        """Custom export action"""
        resource = BookResource()
        dataset = resource.export(queryset)
        response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="books.xlsx"'
        return response
```

## Best Practices

1. Always test imports with `dry_run=True` first
2. Use explicit field declarations for important models
3. Implement proper error handling for imports
4. Consider data validation in `before_import_row`
5. For large datasets, use chunking or background tasks
6. Document expected import/export formats for users

## Troubleshooting

**Issue:** Import fails silently
- Solution: Check `result.has_errors()` and `result.rows` after import

**Issue:** Foreign key relationships fail
- Solution: Use `ForeignKeyWidget` or ensure related objects exist first

**Issue:** Performance problems with large imports
- Solution: Use `--batch-size` parameter or implement chunked imports
