from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger

# Create your views here.
class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset =Post.published.all()
    context_object_name ='posts'
    paginate_by = 5
    template_name = 'blog/post/list.html'

def post_list(request):
     post_list = Post.published.all()
     #paginator with 5 posts per page
     paginator = Paginator(post_list, 5)
     page_number = request.GET.get('page')
     try:
        posts = paginator.page(page_number)
     except PageNotAnInteger:
        #If page_number is not an integer deliver the first page
        posts = paginator.page(1)
     except EmptyPage:
        #if page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
     return render(request,
                  'blog/post/list.html',
                   {'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                            status=Post.Status.PUBLISHED,
                            slug=post,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)

    return render(request,
                'blog/post/detail.html',
                {'post': post})

def post_share(request, post_id):
    #retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        #Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_url(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'rosemaryojwang26@gmail.com',
                      [cd['to']])
            sent = True

        else:
            form = EmailPostForm()

        return render(request, 'blog/post/share.html', {'post': post,
                                                        'form': form,
                                                        'sent': sent})