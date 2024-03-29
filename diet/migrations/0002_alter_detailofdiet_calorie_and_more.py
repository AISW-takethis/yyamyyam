# Generated by Django 5.0 on 2024-02-05 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("diet", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="detailofdiet",
            name="calorie",
            field=models.FloatField(db_comment="1인분당 칼로리"),
        ),
        migrations.AlterField(
            model_name="detailofdiet",
            name="carbohydrate",
            field=models.FloatField(db_comment="1인분당 탄수화물"),
        ),
        migrations.AlterField(
            model_name="detailofdiet",
            name="fat",
            field=models.FloatField(db_comment="1인분당 지방"),
        ),
        migrations.AlterField(
            model_name="detailofdiet",
            name="protein",
            field=models.FloatField(db_comment="1인분당 단백질"),
        ),
        migrations.AlterField(
            model_name="detailofdiet",
            name="quantity",
            field=models.FloatField(
                db_comment="m.n 인분(0.5, 1, 1.5, 2 인분 설정 가능)"
            ),
        ),
        migrations.AlterField(
            model_name="food",
            name="calorie",
            field=models.FloatField(db_comment="1인분당 칼로리"),
        ),
        migrations.AlterField(
            model_name="food",
            name="carbohydrate",
            field=models.FloatField(db_comment="1인분당 탄수화물"),
        ),
        migrations.AlterField(
            model_name="food",
            name="fat",
            field=models.FloatField(db_comment="1인분당 지방"),
        ),
        migrations.AlterField(
            model_name="food",
            name="protein",
            field=models.FloatField(db_comment="1인분당 단백질"),
        ),
    ]
