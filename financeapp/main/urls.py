from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_to_home, name='redirect_to_home'), # Redirects to home
    path('home/', views.home, name='home'), # Home page
    path('accounts/profile/', views.profile, name='profile'), # Profile page
    path('accounts/logout/', views.logout_view, name='logout'), # Logout page
    path('create_portfolio/', views.create_portfolio, name='create_portfolio'), # Create portfolio
    path('delete_portfolio/<int:portfolio_id>/', views.delete_portfolio, name='delete_portfolio'), # Delete portfolio
    path('portfolio/<int:portfolio_id>/', views.portfolio_detail, name='portfolio_detail'), # Portfolio detail
    #path('test_database/', views.test_database, name='test_database'),
]