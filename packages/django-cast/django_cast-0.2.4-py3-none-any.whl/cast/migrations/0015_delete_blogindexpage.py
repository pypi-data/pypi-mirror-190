# Generated by Django 3.2.6 on 2021-08-21 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailredirects", "0006_redirect_increase_max_length"),
        ("wagtailcore", "0062_comment_models_and_pagesubscription"),
        ("wagtailforms", "0004_add_verbose_name_plural"),
        ("cast", "0014_remove_gallery_user"),
    ]

    operations = [
        migrations.DeleteModel(
            name="BlogIndexPage",
        ),
    ]
