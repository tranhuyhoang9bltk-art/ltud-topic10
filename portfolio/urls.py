from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('profile/', views.profile, name='profile'),

    path('portfolio/', views.portfolio, name='portfolio'),

    path('add-project/',
         views.add_project,
         name='add_project'),

    path('edit-project/<int:id>/',
         views.edit_project,
         name='edit_project'),

    path('delete-project/<int:id>/',
         views.delete_project,
         name='delete_project'),
    path('contact/',
         views.contact,
         name='contact'),

    path('blog/',
         views.blog,
         name='blog'),

    path('blog/<int:id>/',
         views.blog_detail,
         name='blog_detail'),

    path('categories/',
         views.categories,
         name='categories'),

    path('gallery/',
         views.gallery,
         name='gallery'),

    path('login/',
         views.login_user,
         name='login'),

    path('logout/',
         views.logout_user,
         name='logout'),

    path('portfolio/<int:id>/',
         views.project_detail,
         name='project_detail'),

    path('skills/',
         views.skills,
         name='skills'),

    path('api/create-booking/',
         views.create_booking,
         name='create_booking'),

    path('<str:page>',
         views.theme_page,
         name='theme_page'),
]
