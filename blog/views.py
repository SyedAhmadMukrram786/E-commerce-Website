from django.shortcuts import render
from django.http import HttpResponse
from .models import Blogpost

# Create your views here.
def index(request):
    blogpost = Blogpost.objects.all()
    if len(blogpost) > 0:
        return render(request, 'blog/index.html',{'blogs':blogpost})
    else:
        return render(request, 'blog/index.html')

def blogpost(request, id):
    post = Blogpost.objects.filter(post_id = id)[0]
    print(post)
    return render(request, 'blog/blogpost.html', {'post': post})
