from django.urls import path, re_path

from . import views


urlpatterns = [
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('account/', views.user_account, name="account"),
    path('account/edit/', views.edit_user, name="edit-user"),
    path('account/edit/email', views.post_change_email_form_j),
    re_path(r'^account/change-email/(?P<key>[^/]+)/confirm$',
            views.confirm_change_email, name='change-email-confirm'),
]