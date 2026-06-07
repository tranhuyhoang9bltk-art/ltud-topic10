from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .models import *

from .forms import ProjectForm

from django.core.paginator import Paginator

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from django.db.utils import OperationalError

import json

THEME_PAGES = {
    'about.html',
    'services.html',
    'pricing.html',
    'portfolio.html',
    'portfolio-details.html',
    'gallery.html',
    'blog-details.html',
    'main.html',
    'blog.html',
    'index.html',
    'profile.html',
}


def home(request):

    profile = None
    skills = []
    projects = []
    blogs = []
    categories = []

    try:
        profile = Profile.objects.first()
        skills = Skill.objects.all()
        categories = Category.objects.all()
        projects = Project.objects.all()[:2]  # Chỉ hiển thị 2 dự án mới nhất trên home page
        blogs = Blog.objects.all()
    except OperationalError:
        # Database tables may not exist yet; show an empty page until migrations are run.
        profile = None
        skills = []
        projects = []
        blogs = []
        categories = []

    return render(request,'portfolio/index.html',{

        'profile': profile,
        'skills': skills,
        'projects': projects,
        'blogs': blogs,
        'categories': categories,
    })


def profile(request):
    """Hiển thị trang profile"""
    page_obj = None
    try:
        profile_data = Profile.objects.first()
        skills = Skill.objects.all()
        page_obj = Page.objects.filter(slug='profile').first()
    except OperationalError:
        profile_data = None
        skills = []
        page_obj = None
    
    return render(request, 'portfolio/profile.html', {
        'profile': profile_data,
        'skills': skills,
        'page_obj': page_obj,
    })


def skills(request):
    """Hiển thị trang kỹ năng riêng"""
    page_obj = None
    try:
        skills = Skill.objects.all()
        page_obj = Page.objects.filter(slug='skills').first()
    except OperationalError:
        skills = []
        page_obj = None
    return render(request, 'portfolio/skills.html', {
        'skills': skills,
        'page_obj': page_obj,
    })


def portfolio(request):
    """Hiển thị trang danh sách tất cả dự án"""
    category_id = request.GET.get('category')
    selected_category = None
    try:
        categories = Category.objects.all()
        if category_id:
            selected_category = Category.objects.filter(id=category_id).first()
            projects = Project.objects.filter(category_id=category_id)
        else:
            projects = Project.objects.all()
    except OperationalError:
        projects = []
        categories = []
        selected_category = None
    
    return render(request, 'portfolio/portfolio.html', {
        'projects': projects,
        'categories': categories,
        'selected_category': selected_category,
    })


def theme_page(request, page):
    if page in THEME_PAGES:
        context = {}
        slug = page.replace('.html', '')
        page_obj = None
        try:
            from .models import Page, AboutContent, AboutFeature, TeamMember, Testimonial, Pricing
            page_obj = Page.objects.filter(slug=slug).first()
            
            # Nếu là trang About, lấy thêm dữ liệu AboutContent, AboutFeature, TeamMember và Testimonial
            if slug == 'about':
                about_content = AboutContent.objects.first()
                about_features = AboutFeature.objects.all()
                team_members = TeamMember.objects.all()
                testimonials = Testimonial.objects.all()
                context['about_content'] = about_content
                context['about_features'] = about_features
                context['team_members'] = team_members
                context['testimonials'] = testimonials

            # Nếu là trang Pricing, lấy dữ liệu từ model Pricing để web hiển thị giá động
            if slug == 'pricing':
                pricing_packages = Pricing.objects.all().order_by('name')
                context['pricing_packages'] = pricing_packages
        except Exception:
            page_obj = None

        context['page_obj'] = page_obj
        return render(request, f'portfolio/{page}', context)
    raise Http404


@login_required
def add_project(request):

    if request.method == 'POST':

        form = ProjectForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect('home')

    else:

        form = ProjectForm()

    return render(request,
    'portfolio/add_project.html',
    {'form':form})


@login_required
def edit_project(request,id):

    project = Project.objects.get(id=id)

    if request.method == 'POST':

        form = ProjectForm(
            request.POST,
            request.FILES,
            instance=project
        )

        if form.is_valid():

            form.save()

            return redirect('home')

    else:

        form = ProjectForm(instance=project)

    return render(request,
    'portfolio/edit_project.html',
    {'form':form})


@login_required
def delete_project(request,id):

    project = Project.objects.get(id=id)

    if request.method == 'POST':
        project.delete()
        return redirect('home')

    return render(request,
    'portfolio/delete_project.html',
    {'project': project})


def contact(request):

    if request.method == 'POST':

        name = request.POST['name']

        email = request.POST['email']

        message = request.POST['message']

        Contact.objects.create(
            name=name,
            email=email,
            message=message
        )

        return render(request, 'portfolio/contact.html', {
            'success': True,
            'success_message': 'Cảm ơn bạn! Tin nhắn của bạn đã được gửi. Admin sẽ liên hệ với bạn sớm.'
        })

    return render(request,'portfolio/contact.html')


def blog(request):

    blog_list = Blog.objects.all()

    paginator = Paginator(blog_list,2)

    page_number = request.GET.get('page')

    blogs = paginator.get_page(page_number)

    return render(request,
    'portfolio/blog.html',
    {'blogs':blogs})


def blog_detail(request, id):
    try:
        post = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        raise Http404
    return render(request, 'portfolio/blog-details.html', {'post': post})


def gallery(request):
    """Hiển thị trang thư viện ảnh"""
    category_id = request.GET.get('category')
    selected_category = None
    try:
        if category_id:
            gallery_items = Gallery.objects.filter(category_id=category_id)
            selected_category = Category.objects.filter(id=category_id).first()
        else:
            gallery_items = Gallery.objects.all()
    except OperationalError:
        gallery_items = []
    
    return render(request, 'portfolio/gallery.html', {
        'gallery_list': gallery_items,
        'selected_category': selected_category,
    })


def categories(request):
    """Hiển thị trang tất cả danh mục"""
    try:
        category_list = Category.objects.all()
    except OperationalError:
        category_list = []
    
    return render(request, 'portfolio/categories.html', {
        'categories': category_list,
    })


def login_user(request):

    if request.method == 'POST':

        username = request.POST['username']

        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request,user)

            return redirect('home')

    return render(request,'portfolio/login.html')


def logout_user(request):

    logout(request)

    return redirect('home')


def project_detail(request, id):
    try:
        project = Project.objects.get(id=id)
    except Project.DoesNotExist:
        raise Http404
    return render(request, 'portfolio/portfolio-details.html', {'project': project})


@require_http_methods(["POST"])
@csrf_exempt
def create_booking(request):
    """Tạo booking và trả về mã QR thanh toán"""
    try:
        data = json.loads(request.body)
        
        package_name = data.get('package')
        customer_name = data.get('customer_name')
        customer_email = data.get('customer_email')
        customer_phone = data.get('customer_phone')
        scheduled_date = data.get('scheduled_date')
        
        # Validate dữ liệu
        if not all([package_name, customer_name, customer_email, customer_phone, scheduled_date]):
            return JsonResponse({
                'success': False,
                'message': 'Vui lòng điền đầy đủ thông tin'
            }, status=400)
        
        # Tìm gói giá
        try:
            package = Pricing.objects.get(name=package_name)
        except Pricing.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Gói dịch vụ không tồn tại'
            }, status=400)
        
        # Tạo booking
        booking = Booking.objects.create(
            package=package,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            scheduled_date=scheduled_date,
            status='pending'
        )
        
        return JsonResponse({
            'success': True,
            'booking_id': booking.id,
            'package_name': package.get_name_display(),
            'price': package.price,
            'message': f'Đặt lịch thành công! ID: {booking.id}'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Dữ liệu không hợp lệ'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }, status=500)