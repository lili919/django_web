from django.shortcuts import render
from .models import BlogArticles


def blog_list(request):
    blogs = BlogArticles.objects.all()
    return render(request, "blog/blog_list.html", {"blogs":blogs})

# Create your views here.
