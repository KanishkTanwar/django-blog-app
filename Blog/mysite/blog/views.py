from django.shortcuts import render, get_object_or_404,redirect
from blog import models
from blog import forms
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView,
                                  DeleteView, CreateView,
                                  UpdateView, DetailView)

# Create your views here.


class AboutView(TemplateView):
    template_name = 'blog/about.html'


class PostListView(ListView):
    model = models.Post

    def get_queryset(self):
        return models.Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = models.Post


class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = forms.PostForm # ye yahan par default banega html name post_form.html
    model = models.Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/' # this will send user if not looged in to login urls but we have declared accounts/login hence cause error

    redirect_field_name = 'app/post_detail.html'# settings.py has default redirect which is removing all instances and overide itself

    form_class = forms.PostForm#fields = ('author', 'title', 'text') # direct fields can pass here we are not passing because we are adding some classes so that medium class editor works
    model = models.Post


class DraftListView(LoginRequiredMixin, ListView):# abhi ye view Postlistview ki template pe send kar raha h to change this you need to give it template name you can check by the data you are passing in that file 3 name file.html and it is not showing anythong just add the template name with this 3 name file name
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = models.Post

    def get_queryset(self):
        return models.Post.objects.filter(published_date__isnull=True).order_by('created_date')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Post
    success_url = reverse_lazy('post_list')# not redirected deleteview need this 
    

#####################
#####################

@login_required
def post_publish(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def add_comment_to_post(request, pk):

    post = get_object_or_404(models.Post, pk=pk)

    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)  # try only pk no change
    else:
        form = forms.CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(models.Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(models.Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


