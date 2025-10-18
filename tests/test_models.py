import pytest
from django.test import TestCase
from django.utils import timezone
from datetime import datetime, timedelta

from django_app.models import Todo


class TestTodoModel(TestCase):

    @pytest.mark.timeout(30)
    def test_todo_str_short_content(self):
        """
        Test kind: unit_tests
        Original method: django_app/models.py::Todo.__str__
        """
        # Create a todo with short content
        todo = Todo(content="Buy groceries")

        # Test that __str__ returns the full content when it's short
        self.assertEqual(str(todo), "Buy groceries")

    @pytest.mark.timeout(30)
    def test_todo_str_long_content(self):
        """
        Test kind: unit_tests
        Original method: django_app/models.py::Todo.__str__
        """
        # Create a todo with content longer than 50 characters
        long_content = "This is a very long todo content that exceeds fifty characters limit"
        todo = Todo(content=long_content)

        # Test that __str__ returns truncated content to 50 characters
        expected = long_content[:50]
        self.assertEqual(str(todo), expected)
        self.assertEqual(len(str(todo)), 50)

    @pytest.mark.timeout(30)
    def test_todo_str_exactly_fifty_chars(self):
        """
        Test kind: unit_tests
        Original method: django_app/models.py::Todo.__str__
        """
        # Create a todo with exactly 50 characters
        content_50_chars = "This content has exactly fifty characters total"  # 46 + 4 = 50
        content_50_chars = "This content is exactly fifty characters in total"  # Let me count: 49 chars
        content_50_chars = "This content is exactly fifty characters in totals"  # 50 chars
        todo = Todo(content=content_50_chars)

        # Test that __str__ returns the full content when exactly 50 chars
        self.assertEqual(str(todo), content_50_chars)
        self.assertEqual(len(str(todo)), 50)

    @pytest.mark.timeout(30)
    def test_is_done_when_not_marked(self):
        """
        Test kind: unit_tests
        Original method: django_app/models.py::Todo.is_done
        """
        # Create a todo without marked_as_done_at
        todo = Todo(content="Test todo", marked_as_done_at=None)

        # Test that is_done returns False
        self.assertFalse(todo.is_done)

    @pytest.mark.timeout(30)
    def test_is_done_when_marked_as_done(self):
        """
        Test kind: unit_tests
        Original method: django_app/models.py::Todo.is_done
        """
        # Create a todo with marked_as_done_at set
        done_time = timezone.now()
        todo = Todo(content="Test todo", marked_as_done_at=done_time)

        # Test that is_done returns True
        self.assertTrue(todo.is_done)

    @pytest.mark.timeout(30)
    def test_is_done_with_past_timestamp(self):
        """
        Test kind: unit_tests
        Original method: django_app/models.py::Todo.is_done
        """
        # Create a todo marked as done in the past
        past_time = timezone.now() - timedelta(days=1)
        todo = Todo(content="Test todo", marked_as_done_at=past_time)

        # Test that is_done returns True
        self.assertTrue(todo.is_done)