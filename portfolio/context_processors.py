from .models import SiteSetting, Hero, Service, Gallery, Project, Blog, Category


def site_settings(request):
    settings = SiteSetting.objects.first()
    heroes = Hero.objects.all()
    services = Service.objects.all()
    gallery = Gallery.objects.filter(featured=True)
    projects = Project.objects.all()
    blogs = Blog.objects.order_by('-created_at')[:10]
    categories = Category.objects.all()
    return {
        'site_settings': settings,
        'hero_list': heroes,
        'services_list': services,
        'gallery_list': gallery,
        'projects': projects,
        'blogs': blogs,
        'categories': categories,
    }
