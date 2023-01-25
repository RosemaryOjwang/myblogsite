from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404

# Create your views here.
def post_list(request):
    posts = get_object_or_404(Post,
                              id=id,
                              status=Post.Status.PUBLISHED)

    return render(request,
                  'blog/post/list.html',
                  {'posts': posts}) 

def post_detail(request, id):
    try:
        post = Post.published.get(id=id)
    except Post.DoesNotExist:
        raise Http404('No post found.')

    return render(request,
                 'blog/post/detail.html',
                 {'post': post}
                )
    