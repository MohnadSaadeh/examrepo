# Generated by Django 5.0.3 on 2024-04-16 18:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tv_app', '0004_rename_description_show_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='tv_app.show')),
            ],
        ),
    ]
