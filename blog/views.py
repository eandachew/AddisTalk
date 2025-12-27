from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post

# List of posts (homepage)
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "blog/index.html"
    context_object_name = "post_list"
    paginate_by = 6


# Detail of a single post
def PostDetail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=1)
    return render(request, "blog/post_detail.html", {"post": post})
