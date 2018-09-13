from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from . import site_settings

from .models import NewsPost

def index(request):

    latest_updates = NewsPost.objects.order_by('-pub_date')[:3]
    context = {
                'latest_updates': latest_updates,
              }

    return render(request, 'oscar/index.html', context)

def post(request, post_id):
    active_post = get_object_or_404(NewsPost, pk=post_id)
    latest_updates = NewsPost.objects.order_by('-pub_date')[:3]
    context = {
                'latest_updates': latest_updates,
                'active_post'   : active_post,
              }

    return render(request, 'oscar/index.html', context)

def blog(request, page_number=1):
    
    latest_updates = NewsPost.objects.order_by('-pub_date')[:3]
    startPost = 0 + (page_number-1) * site_settings.blog_posts_per_page
    blog_post_list = NewsPost.objects.order_by('-pub_date')[startPost:startPost + site_settings.blog_posts_per_page]
    
    next_page_exists = True if (startPost+site_settings.blog_posts_per_page) < NewsPost.objects.count() else False
    prev_page_exists = False if page_number <= 1 else True

    #print("Page number:", page_number)
    #print("startPost:", startPost)
    #print("nextPageExists:", next_page_exists)
    #print("prevPageExists:", prev_page_exists)
    #print("latest_updates", latest_updates)
    #print("blog_post_list", blog_post_list)

    context = {
                'blog_post_list': blog_post_list,
                'latest_updates': latest_updates,
                'next_page_exists': next_page_exists,
                'prev_page_exists': prev_page_exists,
                'current_page': page_number,
              }

    return render(request, 'oscar/index.html', context)