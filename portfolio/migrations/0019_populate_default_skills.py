from django.db import migrations


def populate_default_skills(apps, schema_editor):
    Skill = apps.get_model('portfolio', 'Skill')
    default_skills = [
        {'name': 'Chụp ảnh', 'percent': 95},
        {'name': 'Chỉnh sửa ảnh', 'percent': 90},
        {'name': 'Quay phim', 'percent': 85},
        {'name': 'Lên ý tưởng', 'percent': 80},
    ]
    for data in default_skills:
        Skill.objects.get_or_create(name=data['name'], defaults={'percent': data['percent']})


def reverse_populate_default_skills(apps, schema_editor):
    Skill = apps.get_model('portfolio', 'Skill')
    Skill.objects.filter(name__in=['Chụp ảnh', 'Chỉnh sửa ảnh', 'Quay phim', 'Lên ý tưởng']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0018_populate_testimonials'),
    ]

    operations = [
        migrations.RunPython(populate_default_skills, reverse_populate_default_skills),
    ]
