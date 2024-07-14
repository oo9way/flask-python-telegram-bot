from django.db import models


class Script(models.Model):
    LANGUAGE_CHOICES = (
        ('uz', 'O\'zbek'),
        ('ar', 'Arabic'),
    )
    text = models.TextField()

    text_ar = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)

    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    audio_ar = models.FileField(upload_to='audios', null=True, blank=True)
    audio_uz = models.FileField(upload_to='audios', null=True, blank=True)
    audio_ru = models.FileField(upload_to='audios', null=True, blank=True)

    def __str__(self):
        return self.text[:100]
