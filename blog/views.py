# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
#JsonResponse to return json objects used in infinite scroll
# from django.http import JsonResponse
from django.views.generic import ListView
from .models import Post, Comment
from .forms import CommentForm
from taggit.models import Tag
from django.db.models import Count

#function based view without pagination
# def post_list(request):
#     posts = Post.published.all()
#     return render(request,'blog/post/list.html',{'posts': posts})

#post detail view without comments
# def post_detail(request, year, month, day, post):
#     post = get_object_or_404(Post, slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
#     return render(request,'blog/post/detail.html',{'post': post})

#post detail view with comments
# def post_detail(request, year, month, day, post):
#     post = get_object_or_404(Post, slug=post,
#                                    status='published',
#                                    publish__year=year,
#                                    publish__month=month,
#                                    publish__day=day)
    
#     # List of active comments for this post
#     comments = post.comments.filter(active=True)

#     new_comment = None

#     if request.method == 'POST':
#         # A comment was posted
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             # Create Comment object but don't save to database yet
#             new_comment = comment_form.save(commit=False)
#             # Assign the current post to the comment
#             new_comment.post = post
#             # Save the comment to the database
#             new_comment.save()
#     else:
#         comment_form = CommentForm()
    
#     # List of similar posts
#     post_tags_ids = post.tags.values_list('id', flat=True)
#     similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
#     similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

#     return render(request,
#                   'blog/post/detail.html',
#                   {'post': post,
#                    'comments': comments,
#                    'new_comment': new_comment,
#                    'comment_form': comment_form,
#                    'similar_posts': similar_posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    
    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:3]

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts})


#function based view with pagination
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 2) # 2 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:     
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,'blog/post/list.html',{'page': page,'posts': posts, 'tag': tag})


# def post_list(request, tag_slug=None):
#     object_list = Post.published.all()
#     tag = None

#     if tag_slug:
#         tag = get_object_or_404(Tag, slug=tag_slug)
#         object_list = object_list.filter(tags__in=[tag])

#     paginator = Paginator(object_list, 3) # 3 posts in each page
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer deliver the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)

#     return render(request,
#                   'blog/post/list.html',
#                   {'page': page,
#                    'posts': posts,
#                    'tag': tag})


#class based view with pagination
# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 2
#     template_name = 'blog/post/list.html'

    


