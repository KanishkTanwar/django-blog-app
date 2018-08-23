from django import forms
from blog import models


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ('author', 'title', 'text')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}) # psotcontent is the class for text and this is editable class for that medium style 
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('author', 'text')

        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'})
        }
