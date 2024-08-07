# Generated by Django 4.0 on 2024-07-14 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_script_text_ar_script_text_ru_script_text_uz'),
    ]

    operations = [
        migrations.RenameField(
            model_name='script',
            old_name='audio_file',
            new_name='audio_ar',
        ),
        migrations.AddField(
            model_name='script',
            name='audio_ru',
            field=models.FileField(blank=True, null=True, upload_to='audios'),
        ),
        migrations.AddField(
            model_name='script',
            name='audio_uz',
            field=models.FileField(blank=True, null=True, upload_to='audios'),
        ),
    ]
