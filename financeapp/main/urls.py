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

    #htmx urls
    path('search_stock/', views.search_stock, name='search_stock'),
    path('add_to_portfolio/', views.add_to_portfolio, name='add_to_portfolio'),
    path('remove_from_portfolio/', views.remove_from_portfolio, name='remove_from_portfolio')


    #path('search_stock/', views.search_stock, name='search_stock'), # Create stock
    #path('add_stock/<int:portfolio_id>/', views.add_stock, name='add_stock'), # Add stock
    #path('delete_stock/<int:stock_id>/', views.delete_stock, name='delete_stock'), # Update stock
    #path('stock_list/<int:portfolio_id>/', views.stock_list, name='stock_list'), # Stock list
    #path('test_database/', views.test_database, name='test_database'),
]