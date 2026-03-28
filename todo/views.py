from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q, Count
from .models import Task, Category
import json


# ─── AUTH VIEWS ───────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'todo/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        if password != confirm:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            # Create default categories for new user
            default_categories = [
                {'name': 'Work', 'color': '#6366f1', 'icon': 'briefcase'},
                {'name': 'Personal', 'color': '#10b981', 'icon': 'user'},
                {'name': 'Learning', 'color': '#f59e0b', 'icon': 'book'},
                {'name': 'Health', 'color': '#ef4444', 'icon': 'heart'},
            ]
            for cat in default_categories:
                Category.objects.create(user=user, **cat)
            login(request, user)
            messages.success(request, f'Welcome, {username}!')
            return redirect('dashboard')

    return render(request, 'todo/register.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ─── MAIN DASHBOARD ───────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user)

    # Filters
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    category_filter = request.GET.get('category', '')
    search_query = request.GET.get('q', '')

    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    if category_filter:
        tasks = tasks.filter(category_id=category_filter)
    if search_query:
        tasks = tasks.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    # Stats
    all_tasks = Task.objects.filter(user=request.user)
    stats = {
        'total': all_tasks.count(),
        'completed': all_tasks.filter(completed=True).count(),
        'in_progress': all_tasks.filter(status='in_progress').count(),
        'overdue': sum(1 for t in all_tasks if t.is_overdue),
        'critical': all_tasks.filter(priority='critical', completed=False).count(),
    }
    if stats['total'] > 0:
        stats['completion_rate'] = round((stats['completed'] / stats['total']) * 100)
    else:
        stats['completion_rate'] = 0

    context = {
        'tasks': tasks,
        'categories': categories,
        'stats': stats,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'category_filter': category_filter,
        'search_query': search_query,
        'today': timezone.now().date(),
    }
    return render(request, 'todo/dashboard.html', context)


# ─── TASK CRUD ─────────────────────────────────────────────────────────────────

@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if not title:
            messages.error(request, 'Task title is required.')
            return redirect('dashboard')

        category_id = request.POST.get('category') or None
        due_date = request.POST.get('due_date') or None

        Task.objects.create(
            user=request.user,
            title=title,
            description=request.POST.get('description', ''),
            priority=request.POST.get('priority', 'medium'),
            status=request.POST.get('status', 'todo'),
            category_id=category_id,
            due_date=due_date,
            tags=request.POST.get('tags', ''),
        )
        messages.success(request, 'Task created successfully!')
    return redirect('dashboard')


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    categories = Category.objects.filter(user=request.user)

    if request.method == 'POST':
        task.title = request.POST.get('title', task.title).strip()
        task.description = request.POST.get('description', '')
        task.priority = request.POST.get('priority', 'medium')
        task.status = request.POST.get('status', 'todo')
        task.tags = request.POST.get('tags', '')
        due_date = request.POST.get('due_date') or None
        task.due_date = due_date
        category_id = request.POST.get('category') or None
        task.category_id = category_id
        task.save()
        messages.success(request, 'Task updated successfully!')
        return redirect('dashboard')

    return render(request, 'todo/edit_task.html', {'task': task, 'categories': categories})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    messages.success(request, 'Task deleted.')
    return redirect('dashboard')


@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('dashboard')


@login_required
def toggle_pin(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_pinned = not task.is_pinned
    task.save()
    return redirect('dashboard')


# ─── CATEGORY MANAGEMENT ──────────────────────────────────────────────────────

@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        color = request.POST.get('color', '#6366f1')
        icon = request.POST.get('icon', 'folder')
        if name:
            Category.objects.create(user=request.user, name=name, color=color, icon=icon)
            messages.success(request, f'Category "{name}" created!')
    return redirect('dashboard')


@login_required
def delete_category(request, cat_id):
    category = get_object_or_404(Category, id=cat_id, user=request.user)
    category.delete()
    messages.success(request, 'Category deleted.')
    return redirect('dashboard')


# ─── API ENDPOINTS (for AJAX) ─────────────────────────────────────────────────

@login_required
def api_task_status(request, task_id):
    """AJAX endpoint to update task status"""
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id, user=request.user)
        data = json.loads(request.body)
        task.status = data.get('status', task.status)
        if task.status == 'done':
            task.completed = True
        task.save()
        return JsonResponse({'success': True, 'status': task.status})
    return JsonResponse({'success': False}, status=400)