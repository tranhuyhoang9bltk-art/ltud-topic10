# Generated migration to populate default team members

from django.db import migrations

def populate_team_members(apps, schema_editor):
    """Populate default team members"""
    TeamMember = apps.get_model('portfolio', 'TeamMember')
    
    team_members_data = [
        {
            'name': 'Alan Walker',
            'position': 'Nhiếp ảnh gia',
            'facebook_url': '#',
            'twitter_url': '#',
            'youtube_url': '#',
            'instagram_url': '#',
            'order': 1
        },
        {
            'name': 'Ava Max',
            'position': 'Đạo diễn',
            'facebook_url': '#',
            'twitter_url': '#',
            'youtube_url': '#',
            'instagram_url': '#',
            'order': 2
        },
        {
            'name': 'Anne-Marie',
            'position': 'Quản lý',
            'facebook_url': '#',
            'twitter_url': '#',
            'youtube_url': '#',
            'instagram_url': '#',
            'order': 3
        },
        {
            'name': 'Billie Eilish',
            'position': 'Trợ lý',
            'facebook_url': '#',
            'twitter_url': '#',
            'youtube_url': '#',
            'instagram_url': '#',
            'order': 4
        },
    ]
    
    for member_data in team_members_data:
        TeamMember.objects.get_or_create(
            name=member_data['name'],
            defaults=member_data
        )

def reverse_team_members(apps, schema_editor):
    """Reverse operation"""
    TeamMember = apps.get_model('portfolio', 'TeamMember')
    TeamMember.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0015_teammember'),
    ]

    operations = [
        migrations.RunPython(populate_team_members, reverse_team_members),
    ]
