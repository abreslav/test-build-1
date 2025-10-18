from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .models import Todo


def todo_list(request):
    """Display all todos and handle new todo creation"""
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Todo.objects.create(content=content)
        return redirect('todo_list')

    todos = Todo.objects.all()
    completed_count = todos.filter(marked_as_done_at__isnull=False).count()
    total_count = todos.count()
    remaining_count = total_count - completed_count
    context = {
        'todos': todos,
        'completed_count': completed_count,
        'total_count': total_count,
        'remaining_count': remaining_count
    }
    return render(request, 'django_app/todo_list.html', context)


@require_http_methods(["POST"])
def toggle_todo(request, todo_id):
    """Toggle todo completion status"""
    todo = get_object_or_404(Todo, id=todo_id)

    if todo.is_done:
        todo.marked_as_done_at = None
    else:
        todo.marked_as_done_at = timezone.now()

    todo.save()
    return redirect('todo_list')


@require_http_methods(["POST"])
def delete_todo(request, todo_id):
    """Delete a todo item"""
    todo = get_object_or_404(Todo, id=todo_id)
    todo.delete()
    return redirect('todo_list')
