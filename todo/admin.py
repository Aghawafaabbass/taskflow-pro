from django.contrib import admin
from .models import Task, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'user', 'created_at')
    list_filter = ('user',)
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'priority', 'status', 'category', 'due_date', 'completed', 'created_at')
    list_filter = ('priority', 'status', 'completed', 'category', 'user')
    search_fields = ('title', 'description', 'tags')
    list_editable = ('status', 'priority', 'completed')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    fieldsets = (
        ('Task Info', {
            'fields': ('title', 'description', 'user', 'category')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'completed', 'is_pinned')
        }),
        ('Dates', {
            'fields': ('due_date', 'completed_at')
        }),
        ('Meta', {
            'fields': ('tags',),
            'classes': ('collapse',)
        }),
    )