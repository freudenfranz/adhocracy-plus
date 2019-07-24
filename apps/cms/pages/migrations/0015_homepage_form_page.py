# Generated by Django 2.2.3 on 2019-07-24 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('a4_candy_cms_contacts', '0001_initial'),
        ('a4_candy_cms_pages', '0014_add_teaser'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='form_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='a4_candy_cms_contacts.FormPage'),
        ),
    ]
