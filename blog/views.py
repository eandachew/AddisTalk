from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Post, Comment


class PostList(generic.ListView):
    """
    View to display list of all posts.
    """
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = "blog/index.html"
    context_object_name = 'post_list'


def post_detail(request, slug):
    """
    View to display individual post.
    """
    # Get the post by slug, or return 404 if not found
    post = get_object_or_404(Post, slug=slug, status=1)
    
    # Get approved comments for this post
    comments = post.comments.filter(approved=True)
    
    # Check if current user has liked the post
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = post.likes.filter(id=request.user.id).exists()
    
    # Prepare context to pass to template
    context = {
        'post': post,
        'comments': comments,
        'user_has_liked': user_has_liked,
    }
    
    return render(request, 'blog/post_detail.html', context)


@login_required
def add_comment(request, slug):
    """
    View to handle comment submission.
    """
    post = get_object_or_404(Post, slug=slug, status=1)
    
    if request.method == 'POST':
        body = request.POST.get('body', '').strip()
        
        if body:
            # Create comment but don't approve it yet
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                body=body,
                approved=False  # Requires admin approval
            )
            
            messages.success(
                request, 
                'Your comment has been submitted and is awaiting approval.'
            )
        else:
            messages.error(request, 'Comment cannot be empty.')
    
    return redirect('post_detail', slug=post.slug)
