from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('', RedirectView.as_view(url='/accounts/dashboard')),

    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('forgotPassword/', views.forgotPassword, name="forgotPassword"),
    path('reset_password_varidate/<uidb64>/<token>', views.reset_password_varidate, name="reset_password_varidate"),
    path('resetPassword/', views.resetPassword, name="resetPassword"),
]
