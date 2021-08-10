from django import forms

from blog.models import Comment
from blog.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('commenter_name', 'author', 'content')
