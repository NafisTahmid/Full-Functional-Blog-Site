from django.urls import path
from Blog import views
app_name = 'Blog'
urlpatterns = [
    path('', views.blog_list, name="blog_list"),
    # path('',  views.BlogList.as_view(), name="blog_list"),
    path('write/', views.CreateBlog.as_view(), name="create_blog"),
    path('details/<str:slug>/', views.blog_details, name="blog_details"),
    path('liked/<pk>/', views.liked, name="liked_post"),
    path('unliked/<pk>/', views.unliked, name="unliked_post"),
    # path('user-blogs/', views.MyBlogs.as_view(), name="user_blog"),
    path('my-blogs/', views.my_blogs, name='user_blog'),
    path('edit-blog/<pk>/', views.EditBlog.as_view(), name="edit_blog"),
    path('delete-blog/<pk>/', views.DeleteBlog.as_view(), name="delete_blog"),
    path('delete-success/', views.DeleteSuccess.as_view(), name="delete_success"),
    path('create-category/', views.CreateCategory.as_view(), name='create_category'),
    path('all-categories/', views.ShowCategory.as_view(), name='all_categories'),
    path('show-all-categories/<pk>', views.show_all_categories, name='show_all_categories'),
    path('update-category/<pk>', views.EditCategory.as_view(), name='update_category'),
    path('user-categories/', views.MyCategories.as_view(), name='user_categories'),
    path('delete-category/<pk>', views.DeleteCategory.as_view(), name='delete_category')
    # path('category/<str:category>/', views.category_view, name='blog_category'),
    # path('all-categories/', views.AllCategories.as_view(), name="all_categories"),
    # path('category_view/<int:category>', views.category_view, name="category_view")

]