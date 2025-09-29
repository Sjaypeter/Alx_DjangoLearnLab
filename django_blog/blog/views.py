from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from . models import Post, Comment
from .forms import CommentForm
from .serializers import PostSerilizer
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
# Create your views here.

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'blog/templates/register.html'
#This usercreation orm handles user registration and when a user is registered they are redirected to the login page using the successurl



#This creates views that allows authenticated users to view their profile
@login_required
def profile_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("profile")  # Reloads the profile page
    else:
        form = AuthenticationForm()

    return render(request, "blog/templates/profile.html", {"form": form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            form = AuthenticationForm()
            return render('blog/templates/login.html', {'form': form})
        
def logout_view(request):
    logout(request)
    return render(request, 'blog/templates/logout.html')


class ListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerilizer
    model = Post
    template_name = 'blog/post_list.html'
    
class DetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerilizer
    model = Post
    template_name = 'blog/post_detail.html'
    
 #Create View requires login   
class CreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerilizer
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_create.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
#update view requires login and ownership check    
class UpdateView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerilizer
    fields = ['title', 'content']
    template_name = 'blog/post_create.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
class DeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerilizer
    
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('post_list')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    

class BlogCommentCreateView(CreateView, LoginRequiredMixin):
    model = Comment
    template_name = 'blog/post_detail.html'
    form_class = CommentForm
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['pk']) #set post from URL pk
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})
    
    
class BlogCommentUpdateView(UpdateView, LoginRequiredMixin):
    model = Comment
    template_name = 'blog/comment_form.html'
    form_class = CommentForm
    
    def get_success_url(self):
        return reverse_lazy('post_detail',kwargs={'pk': self.kwargs['pk']})
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    
class BlogCommentDeleteView(DeleteView, LoginRequiredMixin):
    model = Comment
    template_name = 'blog/comment_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('post_detail',kwargs={'pk': self.kwargs['pk']})
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
 
 
class SearchView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            #filter post where title, content or tags match query
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
             ).distinct() #distinct avoid duplicate posts
        return Post.objects.all() #returns all post if no query
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get('q', '') #Pass query to template for display
        return context
    
    
class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    
    def get_queryset(self):
        tag_name = self.kwargs['tag_name']
        return Post.objects.filter(tags__name=tag_name) #filters post by exact tag name
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_name'] = self.kwargs['tag_name']
        return context