from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.generic import (ListView, CreateView, TemplateView, )
from django.views.generic.detail import DetailView
from django.views.generic.edit import (UpdateView, DeleteView, )

from blog.models import Post


class PostListView(ListView):
    """Blog blog home page view with pagination."""

    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(posts, self.paginate_by)

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context['posts'] = posts
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Post create view with all model fields."""

    model = Post
    template_name = 'blog/post_create.html'
    fields = '__all__'
    success_url = reverse_lazy('blog:post-list')


class PostDetailView(DetailView):
    """Post details view accessed by primary key."""

    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    extra_context = {'some': 'here we can add extra context from DetailView'}

    @never_cache
    def dispatch(self, *args, **kwargs):
        return super(PostDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    # def post_detail(self, request, pk):
    #     post = Post.objects.get(pk=pk)
    #
    #     # We create empty form when user visits a page
    #     form = CommentForm()
    #     if request.method == 'POST':
    #         form = CommentForm(request.POST)
    #         if form.is_valid():
    #             comment = Comment(
    #                 author=form.cleaned_data['author'],
    #                 content=form.cleaned_data['content'],
    #                 post=post
    #             )
    #             comment.save()
    #
    #     comments = Comment.objects.filter(post=post)
    #     context = {
    #         'post': post,
    #         'comments': comments,
    #         'form': form,
    #     }
    #     return render(request, 'blog/post_detail.html', context)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_update.html'
    context_object_name = 'post'
    fields = ('title', 'content', 'categories')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('blog:post-list')


class BlogCategory(TemplateView):
    """It takes a category name as an argument and
    query the Post database for all posts that have been assigned
    the given category."""

    template_name = 'blog/post_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = kwargs.get('category')
        context['posts'] = Post.objects. \
            filter(categories__name__contains=context['category'])
        return context
