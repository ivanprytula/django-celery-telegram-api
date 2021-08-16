from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import FormMixin
from django.views.generic.edit import UpdateView

from blog.forms import CommentForm
from blog.models import Post


class PostListView(ListView):
    """Blog home page view with pagination."""

    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        search_fields = ['title', 'content', 'categories__name']

        if query:
            object_list = Post.objects.filter(
                Q(title__icontains=query)
                | Q(content__icontains=query)
                | Q(categories__name__icontains=query)
            ).order_by(*search_fields).distinct(*search_fields)
        else:
            object_list = Post.objects.all()
        return object_list

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


class PostDetailView(FormMixin, DetailView):
    """Post details view accessed by primary key."""

    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    form_class = CommentForm
    extra_context = {'some': 'here we can add extra context from DetailView'}

    def __init__(self):
        super().__init__()
        self.object = None

    @never_cache
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post-detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['comments'] = self.object.comments.filter(active=True)
        context['now'] = timezone.now()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Create Comment object but don't save to database yet
        new_comment = form.save(commit=False)
        # Assign the current post to the comment
        new_comment.post = self.object
        # Save the comment to the database
        form.save()
        return super().form_valid(form)


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
