# Generated by Django 4.2.1 on 2023-05-25 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("realstate", "0004_alter_biensimmobilier_prix"),
    ]

    operations = [
        migrations.AddField(
            model_name="biensimmobilier",
            name="nom",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
