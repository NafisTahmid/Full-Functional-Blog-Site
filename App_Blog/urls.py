from django.contrib import admin
from django.urls import path, include
from App_Blog import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('App_Login.urls')),
    path('blog/', include('Blog.urls')),
    path('', views.Index, name="index"),

    

 # Password reset
    path("password-reset/",auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/",auth_views.PasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)