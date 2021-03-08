from django.urls import path, include
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', views.index, name="home_page"),
    path('ref/<str:ref_code>/', views.index, name="home_page"),
    path('about/', views.about, name="about_page"),
    path('contacts/', views.contacts, name="contacts_page"),
    path('stats/', views.stats, name="stats_page"),
    path('login/', views.login, name="login_page"),
    path('signup/', views.signup, name="signup_page"),
    path('recovery/', views.PasswordResetingView.as_view(template_name='frontend/recovery.html'), name="recovery_page"),
    path('terms/', views.terms, name="terms_page"),

    path('view/<str:ads_id><str:ad_id>', views.view, name="view_page"),

    path('account/', views.account, name="account_page"),
    path('viewads/', views.viewads, name="viewads_page"),
    path('viewads/add/', views.viewads_add, name="viewads_add_page"),
    path('referrals/', views.referrals, name="referrals_page"),
    path('insert/', views.insert, name="insert_page"),
    path('payment/', views.payment, name="payment_page"),
    path('exchange/', views.exchange, name="exchange_page"),
    path('plans/', views.plans, name="plans_page"),
    path('exit/',  LogoutView.as_view(), name="exit_page"),
    path('settings/', views.settings, name="settings_page"),

    path('favicon.ico',
        RedirectView.as_view(
            url=staticfiles_storage.url('favicon.ico'),
        ),
        name="favicon"
    ),
    path("robots.txt", views.robots_txt),

]
