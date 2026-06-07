# Generated manually for SiteSetting footer fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0021_skill_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesetting',
            name='footer_heading',
            field=models.CharField(blank=True, help_text='Tiêu đề phần footer ở cột trái', max_length=200),
        ),
        migrations.AddField(
            model_name='sitesetting',
            name='footer_description',
            field=models.TextField(blank=True, help_text='Mô tả ngắn phần footer ở cột trái'),
        ),
    ]
