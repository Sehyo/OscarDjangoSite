from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from . import site_settings
from . import googleOAuthHandler
from datetime import datetime

from .models import NewsPost

def index(request):
    latest_updates = NewsPost.objects.order_by('-pub_date')[:3]
    context = {
                'latest_updates': latest_updates,
                'google_client_id' : site_settings.google_client_id,
              }

    return render(request, 'oscar/index.html', context)

def post(request, post_id):
    active_post = get_object_or_404(NewsPost, pk=post_id)
    latest_updates = NewsPost.objects.order_by('-pub_date')[:3]
    context = {
                'latest_updates': latest_updates,
                'active_post'   : active_post,
                'google_client_id' : site_settings.google_client_id,
              }

    return render(request, 'oscar/index.html', context)

def blog(request, page_number=1):
    
    latest_updates = NewsPost.objects.order_by('-pub_date')[:3]
    startPost = 0 + (page_number-1) * site_settings.blog_posts_per_page
    blog_post_list = NewsPost.objects.order_by('-pub_date')[startPost:startPost + site_settings.blog_posts_per_page]
    
    next_page_exists = True if (startPost+site_settings.blog_posts_per_page) < NewsPost.objects.count() else False
    prev_page_exists = False if page_number <= 1 else True

    context = {
                'blog_post_list': blog_post_list,
                'latest_updates': latest_updates,
                'next_page_exists': next_page_exists,
                'prev_page_exists': prev_page_exists,
                'current_page': page_number,
                'google_client_id' : site_settings.google_client_id,
              }

    return render(request, 'oscar/index.html', context)

def book(request):

    print("HELLO")
    context = {}
    if request.method == 'POST':
        print("POST Request")
        print("name: " + request.POST["name"])
        # 2018-10-12T13:13  <-- Format
        booking_start = datetime.strptime(request.POST["booking_start"], '%Y-%m-%dT%H:%M')
        booking_end = datetime.strptime(request.POST["booking_end"], '%Y-%m-%dT%H:%M')
        
        # Check that end time is not earlier than start time.
        if (booking_end < booking_start) or booking_start < datetime.now():
            context = {
                'google_client_id' : site_settings.google_client_id,
                'book' : True,
                'invalid_dates' : True,
              }
        else:
            # Let's check that there are no conflicting bookings already.
            gOAuthHandler = googleOAuthHandler.GOAuthHandler()
            events = gOAuthHandler.getUpcomingEvents()
            conflictingEventExists = False
            if not events:
                print("No upcoming events found.")
            for event in events:
                start = event["start"].get("dateTime")
                end = event["end"].get("dateTime")
                dStart = datetime.strptime(start[:-9], '%Y-%m-%dT%H:%M')
                dEnd = datetime.strptime(end[:-9], '%Y-%m-%dT%H:%M')
                # Check if selected date is inside this interval.
                if (booking_end > dEnd > booking_start) or booking_end > dStart > booking_start:
                    conflictingEventExists = True
                    break
            
            if conflictingEventExists:
                context = {
                    'google_client_id' : site_settings.google_client_id,
                    'book' : True,
                    'conflicts' : True,
                  }
            else:
                gOAuthHandler.createEvent(request.POST["booking_start"], request.POST["booking_end"], request.POST["name"])
                context = {
                    'google_client_id' : site_settings.google_client_id,
                    'book' : True,
                    'bookingPerformed' : True,
                  }
    else:
        print("Not a POST Request")
        context = {
                    'google_client_id' : site_settings.google_client_id,
                    'book' : True,
                  }
    print(context)

    return render(request, 'oscar/index.html', context)