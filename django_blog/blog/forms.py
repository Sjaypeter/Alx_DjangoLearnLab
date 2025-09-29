from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]  # exclude 'author'

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title

#Form for the Post model using Django’s ModelForm to handle the creation and updating of blog posts.
# Ensures the form validates data properly and includes fields for title, content, 
# and automatically set author based on the logged-in user



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        
    def clean_content(self):
        content = self.cleaned_data.get('content')
        
        if len(content.strip()) < 5:
            raise forms.ValidationError("Comment must be at least 5 characters long")
        
        return content
        
        
#Develop a CommentForm using Django’s ModelForm to facilitate comment creation and updating.
# Ensuring it includes validation rules as necessary.
    