from django import forms
from Blog.models import Blog, Comment, Query

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment', )


class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ('query',)