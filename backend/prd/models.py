from django.db import models
from django.conf import settings

class PRD(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('approved', 'Approved'),
        ('implemented', 'Implemented'),
    )

    title = models.CharField(max_length=255)
    version = models.CharField(max_length=50, default='1.0.0')
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prds')
    repository = models.ForeignKey('github.Repository', on_delete=models.SET_NULL, null=True, blank=True, related_name='prds')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        unique_together = ['title', 'version']

    def __str__(self):
        return f"{self.title} v{self.version}"
