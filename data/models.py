from django.db import models


class Script(models.Model):
    LANGUAGE_CHOICES = (
        ('uz', 'O\'zbek'),
        ('ar', 'Arabic'),
    )
    text = models.TextField()
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    audio_file = models.FileField(upload_to='audios', null=True, blank=True)

    def __str__(self):
        return self.text[:100]
