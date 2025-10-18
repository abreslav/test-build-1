from django.db import models
from django.utils import timezone


class Todo(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    marked_as_done_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content[:50]

    @property
    def is_done(self):
        return self.marked_as_done_at is not None
