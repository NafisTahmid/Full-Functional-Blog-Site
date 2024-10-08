from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView, View
from Blog.models import Blog, Comment, Likes, Category, Query
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
from Blog.forms import CommentForm, QueryForm
from django.core.paginator import Paginator
import openai
from selenium import webdriver
from time import sleep
import requests

# Create your views here.
# Create your views here.
def blog_list(request):
    queryset = Blog.objects.all().order_by('-publish_date')
    per_page = 3
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")
    blogs = paginator.get_page(page_number)
    context = {'blogs':blogs}
    return render(request, 'App_Blog/blog_list.html', context=context)

class CreateBlog(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ('blog_title', 'blog_category', 'blog_content', 'blog_image')
    template_name = "App_Blog/create_blog.html"

    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        title = blog_obj.blog_title
        blog_obj.slug = title.replace(' ', '-') + '-' + str(uuid.uuid4())
        blog_obj.save()
        return HttpResponseRedirect(reverse('index'))
    

class BlogList(ListView):
    model = Blog
    template_name = "App_Blog/blog_list.html"
    context_object_name = "blogs"

@login_required
def blog_details(request, slug):
    blog = Blog.objects.get(slug=slug)
    already_liked = Likes.objects.filter(blog=blog, user=request.user)
    if already_liked:
        liked = True
    else:
        liked= False

    comment = CommentForm()
    if request.method == 'POST':
        comment = CommentForm(request.POST)
        if comment.is_valid():
            comment = comment.save(commit = False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect(reverse('Blog:blog_details', kwargs={'slug': slug}))
        
    app_url = "https://www.themealdb.com/api/json/v1/1/random.php"
    r = requests.get(app_url)
    meal = r.json().get("meals")
    meal_name = meal[0].get('strMeal')
    meal_recipe = meal[0].get('strInstructions')
    return render(request, 'App_Blog/blog_details.html', context={'blog':blog, 'form':comment, 'liked':liked, 'meal_name':meal_name, 'meal_recipe':meal_recipe})

@login_required
def liked(request, pk):
    blog = Blog.objects.get(pk = pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog, user=user)
    if not already_liked:
        liked_post = Likes(blog=blog, user=user)
        liked_post.save()
    return HttpResponseRedirect(reverse('Blog:blog_details', kwargs={'slug': blog.slug}))

@login_required
def unliked(request, pk):
    blog = Blog.objects.get(pk = pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog, user=user)
    if already_liked:
        already_liked.delete()

    return HttpResponseRedirect(reverse('Blog:blog_details', kwargs={'slug': blog.slug}))

class MyBlogs(LoginRequiredMixin, TemplateView):
    template_name = "App_Blog/my_blogs.html"

@login_required
def my_blogs(request):
    queryset = Blog.objects.filter(author = request.user)
    per_page = 3
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")
    blogs = paginator.get_page(page_number)
    context = {'blogs':blogs}
    return render(request, 'App_Blog/my_blogs.html', context=context)

class EditBlog(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ('blog_title', 'blog_category', 'blog_content', 'blog_image')
    template_name = 'App_Blog/edit_blog.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy("Blog:user_blog")
    

class DeleteBlog(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name = "App_Blog/delete_blog.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy("Blog:delete_success")
    
class DeleteSuccess(LoginRequiredMixin, TemplateView):
     template_name = "App_Blog/delete_success.html"

# class AllCategories(LoginRequiredMixin, ListView):
#     model = Blog
#     template_name = "App_Blog/categories.html"
#     context_object_name = "categories"

#     def get_queryset(self):
#         return Blog.choices 

# @login_required
# def category_view(request, category):
#     queryset = Blog.objects.filter(blog_category=category)
#     per_page = 3
#     paginator = Paginator(queryset, per_page)
#     page_number = request.GET.get("page")
#     blogs = paginator.get_page(page_number)
#     context = {'blogs':blogs}
#     return render(request, 'App_Blog/category.html', context={'blogs': blogs, 'category':category})

class CreateCategory(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'App_Blog/create_category.html'
    fields = ('category_name', 'category_image',)
    def form_valid(self, form):
        user_obj = form.save(commit = False)
        user_obj.user = self.request.user
        user_obj.save()
        return HttpResponseRedirect(reverse('Blog:blog_list'))
    

class ShowCategory(LoginRequiredMixin, ListView):
    model = Category
    template_name = "App_Blog/category_list.html"
    context_object_name = "categories"


@login_required
def show_all_categories(request, pk):
    category = Category.objects.get(pk = pk)
    queryset = Blog.objects.filter(blog_category = category)
    per_page = 3
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")
    blogs = paginator.get_page(page_number)
    context = {'blogs':blogs}
    return render(request, 'App_Blog/category_sorted.html', context=context)

class MyCategories(LoginRequiredMixin, TemplateView):
    template_name = 'App_Blog/user_categories.html'

class EditCategory(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ('category_name', 'category_image',)
    template_name = 'App_Blog/create_category.html'

    def get_success_url(self, **kwargs):
        return reverse('Blog:show_all_categories', kwargs={'pk': self.object.pk})
    

class DeleteCategory(LoginRequiredMixin, DeleteView):
     model = Category
     template_name = "App_Blog/delete_blog.html"

     def get_success_url(self, **kwargs):
        return reverse_lazy("Blog:delete_success")
     


@login_required
def ask_ai(request):
    def oai_answer(prompt):
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use the correct model name
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=100,  # Increase this as per your requirements
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        output = response['choices'][0]['message']['content']
        return output

    form = QueryForm()
    answer = ""
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            query = form.save(commit=False)
            query.user = request.user
            query.save()
            question = query.query
            answer = oai_answer(question)
            
    return render(request, "App_Blog/query.html", context={'form': form, 'answer': answer})

# @login_required
# def ask_ai(request):
#     def oai_answer(prompt): 
#         response = openai.Completion.create(
#             model="gpt-4o-mini",
#             prompt=prompt,
#             temperature=0.7,
#             max_tokens=1,
#             top_p=1,
#             frequency_penalty=0,
#             presence_penalty=0
#         )
#         output = response.get('choices')[0].get('text')
#         return output
#     form = QueryForm()
#     answer = ""
#     if request.method == 'POST':
#         form = QueryForm(request.POST)
#         if form.is_valid():
#             query = form.save(commit=False)
#             query.user = request.user
#             query.save()
#             question = query.query
#             answer = oai_answer(question)
#     return render(request, "App_Blog/query.html", context={'form':form, 'answer':answer})

@login_required
def know_location(request):
    driver = webdriver.Chrome()
    url = driver.get('https://www.google.com/maps/@23.7745566,90.4408048,15z?entry=ttu&g_ep=EgoyMDI0MTAwMi4xIKXMDSoASAFQAw%3D%3D')
    sleep(3)
    return render(request, 'App_Blog/maps.html', context={'url':url})


def homepage_banner(request):
    app_url = "https://www.themealdb.com/api/json/v1/1/lookup.php?i=52772"
    r = requests.get(app_url)
    meal = r.json().get("meals")
    meal_name = meal[0].get('strMeal')
    meal_instructions = meal[0].get('strInstructions')
    return render(request, 'base.html', context={'meal_name':meal_name, 'meal_instructions':meal_instructions})

	
