from django import forms

from blog.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class CommentForm(forms.Form):
    """The author field has the forms.TextInput widget. This tells Django to load this field as an HTML text input
    element in the templates. The content field uses a forms.TextArea widget instead, so that the field is rendered as
    an HTML text area element.
    These widgets also take an argument attrs, which is a dictionary and allows us to specify some CSS classes,
    which will help with formatting the template for this view later. It also allows us to add some placeholder text.
    """

    author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Your Name"
        })
    )
    content = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Leave a comment!"
        })
    )
