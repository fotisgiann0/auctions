# Generated by Django 4.2.11 on 2024-04-22 10:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_bid_bid_by_alter_comments_comment_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid_by',
            field=models.ForeignKey(db_column='bid_by', on_delete=django.db.models.deletion.CASCADE, related_name='bid_by_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comments',
            name='comment_by',
            field=models.ForeignKey(db_column='comment_by', on_delete=django.db.models.deletion.CASCADE, related_name='comment_by_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='listing_by',
            field=models.ForeignKey(db_column='listing_by', on_delete=django.db.models.deletion.CASCADE, related_name='listing_by_user', to=settings.AUTH_USER_MODEL),
        ),
    ]