from django.db import migrations, models
import django.db.models.deletion
from django.utils import timezone

def set_existing_news_to_approved(apps, schema_editor):
    News = apps.get_model('news', 'News')
    News.objects.all().update(
        status='APPROVED',
        approved_at=timezone.now()
    )

class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_news_featured_image'),  # Replace with your last migration
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='status',
            field=models.CharField(
                choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')],
                default='PENDING',
                max_length=10
            ),
        ),
        migrations.AddField(
            model_name='news',
            name='approved_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='approved_news',
                to='auth.user'
            ),
        ),
        migrations.AddField(
            model_name='news',
            name='approved_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='news',
            name='review_notes',
            field=models.TextField(blank=True, help_text='Feedback for rejected articles'),
        ),
        migrations.RunPython(set_existing_news_to_approved),
    ] 