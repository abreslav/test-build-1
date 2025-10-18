import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from django_app.models import Todo


class TestTodoViews(TestCase):

    def setUp(self):
        """Set up test client and test data"""
        self.client = Client()
        # Create test todos
        self.todo1 = Todo.objects.create(content="First todo")
        self.todo2 = Todo.objects.create(
            content="Second todo",
            marked_as_done_at=timezone.now()
        )

    @pytest.mark.timeout(30)
    def test_delete_todo_success(self):
        """
        Test kind: endpoint_tests
        Original method: django_app/views.py::delete_todo
        """
        # Ensure the todo exists
        self.assertTrue(Todo.objects.filter(id=self.todo1.id).exists())

        # Make POST request to delete the todo
        response = self.client.post(reverse('delete_todo', args=[self.todo1.id]))

        # Test response redirects to todo_list
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo_list'))

        # Test that the todo is deleted from database
        self.assertFalse(Todo.objects.filter(id=self.todo1.id).exists())

    @pytest.mark.timeout(30)
    def test_delete_todo_nonexistent(self):
        """
        Test kind: endpoint_tests
        Original method: django_app/views.py::delete_todo
        """
        # Try to delete a non-existent todo
        nonexistent_id = 99999
        response = self.client.post(reverse('delete_todo', args=[nonexistent_id]))

        # Should return 404
        self.assertEqual(response.status_code, 404)

    @pytest.mark.timeout(30)
    def test_delete_todo_get_method_not_allowed(self):
        """
        Test kind: endpoint_tests
        Original method: django_app/views.py::delete_todo
        """
        # Try to delete with GET method (should be POST only)
        response = self.client.get(reverse('delete_todo', args=[self.todo1.id]))

        # Should return 405 Method Not Allowed
        self.assertEqual(response.status_code, 405)

    @pytest.mark.timeout(30)
    def test_todo_list_get_displays_todos(self):
        """
        Test kind: endpoint_tests
        Original method: django_app/views.py::todo_list
        """
        response = self.client.get(reverse('todo_list'))

        # Test response is successful
        self.assertEqual(response.status_code, 200)

        # Test that todos are in context
        self.assertIn('todos', response.context)
        self.assertIn('completed_count', response.context)
        self.assertIn('total_count', response.context)
        self.assertIn('remaining_count', response.context)

        # Test the counts
        self.assertEqual(response.context['total_count'], 2)
        self.assertEqual(response.context['completed_count'], 1)  # todo2 is marked as done
        self.assertEqual(response.context['remaining_count'], 1)  # todo1 is not done

        # Test that both todos are in the queryset
        todos = list(response.context['todos'])
        self.assertEqual(len(todos), 2)

    @pytest.mark.timeout(30)
    def test_todo_list_post_creates_todo(self):
        """
        Test kind: endpoint_tests
        Original method: django_app/views.py::todo_list
        """
        initial_count = Todo.objects.count()

        # Post new todo
        response = self.client.post(reverse('todo_list'), {
            'content': 'New todo item'
        })

        # Test response redirects to todo_list
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo_list'))

        # Test that todo was created
        self.assertEqual(Todo.objects.count(), initial_count + 1)
        new_todo = Todo.objects.filter(content='New todo item').first()
        self.assertIsNotNone(new_todo)
        self.assertIsNone(new_todo.marked_as_done_at)

    @pytest.mark.timeout(30)
    def test_todo_list_post_empty_content(self):
        """
        Test kind: endpoint_tests
        Original method: django_app/views.py::todo_list
        """
        initial_count = Todo.objects.count()

        # Post empty content
        response = self.client.post(reverse('todo_list'), {
            'content': ''
        })

        # Test response redirects to todo_list
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo_list'))

        # Test that no todo was created
        self.assertEqual(Todo.objects.count(), initial_count)

    @pytest.mark.timeout(30)
    def test_todo_list_post_whitespace_only_content(self):
        """
        Test kind: endpoint_tests
        Original method: django_app/views.py::todo_list
        """
        initial_count = Todo.objects.count()

        # Post whitespace-only content
        response = self.client.post(reverse('todo_list'), {
            'content': '   \n\t  '
        })

        # Test response redirects to todo_list
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo_list'))

        # Test that no todo was created
        self.assertEqual(Todo.objects.count(), initial_count)

    @pytest.mark.timeout(30)
    def test_toggle_todo_mark_as_done(self):
        """
        Test kind: endpoint_tests
        Original method: django_app/views.py::toggle_todo
        """
        # Ensure todo1 is not done initially
        self.assertIsNone(self.todo1.marked_as_done_at)
        self.assertFalse(self.todo1.is_done)

        # Post to toggle todo
        response = self.client.post(reverse('toggle_todo', args=[self.todo1.id]))

        # Test response redirects to todo_list
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo_list'))

        # Refresh todo from database
        self.todo1.refresh_from_db()

        # Test that todo is now marked as done
        self.assertIsNotNone(self.todo1.marked_as_done_at)
        self.assertTrue(self.todo1.is_done)

    @pytest.mark.timeout(30)
    def test_toggle_todo_unmark_as_done(self):
        """
        Test kind: endpoint_tests
        Original method: django_app/views.py::toggle_todo
        """
        # Ensure todo2 is done initially
        self.assertIsNotNone(self.todo2.marked_as_done_at)
        self.assertTrue(self.todo2.is_done)

        # Post to toggle todo
        response = self.client.post(reverse('toggle_todo', args=[self.todo2.id]))

        # Test response redirects to todo_list
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo_list'))

        # Refresh todo from database
        self.todo2.refresh_from_db()

        # Test that todo is now not marked as done
        self.assertIsNone(self.todo2.marked_as_done_at)
        self.assertFalse(self.todo2.is_done)

    @pytest.mark.timeout(30)
    def test_toggle_todo_nonexistent(self):
        """
        Test kind: endpoint_tests
        Original method: django_app/views.py::toggle_todo
        """
        # Try to toggle a non-existent todo
        nonexistent_id = 99999
        response = self.client.post(reverse('toggle_todo', args=[nonexistent_id]))

        # Should return 404
        self.assertEqual(response.status_code, 404)

    @pytest.mark.timeout(30)
    def test_toggle_todo_get_method_not_allowed(self):
        """
        Test kind: endpoint_tests
        Original method: django_app/views.py::toggle_todo
        """
        # Try to toggle with GET method (should be POST only)
        response = self.client.get(reverse('toggle_todo', args=[self.todo1.id]))

        # Should return 405 Method Not Allowed
        self.assertEqual(response.status_code, 405)