from django.urls import path
from . import views

app_name = 'oscar'
urlpatterns = [path('', views.index, name='index'),
               path('blog/', views.blog, name='blog'),
               path('blog/<int:page_number>/', views.blog, name='blog'),
               path('post/<int:post_id>/', views.post, name='post'),
               path('book/', views.book, name='book'),]