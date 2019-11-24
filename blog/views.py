from django.contrib.auth import authenticate, login
from django.views import generic
from .models import Post
from .forms import CommentForm, PostForm
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegisterView(generic.View):
    def get(self, request):
        return render(request, 'register.html', { 'form': UserCreationForm() })

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(reverse('login'))

        return render(request, 'register.html', { 'form': form })

class LoginView(generic.View):
    def get(self, request):
        return render(request, 'login.html', { 'form':  AuthenticationForm })

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )

            if user is None:
                return render(
                    request,
                    'login.html',
                    { 'form': form, 'invalid_creds': True }
                )

            try:
                form.confirm_login_allowed(user)
            except ValidationError:
                return render(
                    request,
                    'login.html',
                    { 'form': form, 'invalid_creds': True }
                )
            login(request, user)

            return redirect(reverse('home'))

class PostList(generic.ListView):
    queryset = Post.objects.all().order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 3


# class PostDetail(generic.DetailView):
#     model = Post
#     template_name = 'post_detail.html'

def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})

def new_post(request):
    template_name = 'new_post.html'
    new_post = None
    if request.method == 'POST':
        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user
            new_post.slug = slugify(new_post.title)
            new_post.save()
    else:
        post_form = PostForm()

    return render(request, template_name, {'post_form': post_form,'new_post':new_post})


'''
SLUG UTIL
'''




def slugify(text):
    non_url_safe = ['"', '#', '$', '%', '&', '+',
                    ',', '/', ':', ';', '=', '?',
                    '@', '[', '\\', ']', '^', '`',
                    '{', '|', '}', '~', "'"]
    """
    Turn the text content of a header into a slug for use in an ID
    """
    non_safe = [c for c in text if c in non_url_safe]
    if non_safe:
        for c in non_safe:
            text = text.replace(c, '')
    # Strip leading, trailing and multiple whitespace, convert remaining whitespace to _
    text = u'_'.join(text.split())
    return text