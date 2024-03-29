# Generated by Django 5.0.1 on 2024-02-20 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("diet", "0004_remove_food_created_at_remove_food_deleted_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="detailofdiet",
            name="image_x_end",
        ),
        migrations.RemoveField(
            model_name="detailofdiet",
            name="image_x_start",
        ),
        migrations.RemoveField(
            model_name="detailofdiet",
            name="image_y_end",
        ),
        migrations.RemoveField(
            model_name="detailofdiet",
            name="image_y_start",
        ),
        migrations.AddField(
            model_name="detailofdiet",
            name="image_path",
            field=models.CharField(
                db_comment="음식 이미지 경로", default=1, max_length=200
            ),
            preserve_default=False,
        ),
    ]
