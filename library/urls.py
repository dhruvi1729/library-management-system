from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Homepage
    path('admin/signup/', views.admin_signup_page, name='sign_up'),  # Admin signup page
    path('login/', views.admin_login_page, name='login'),  # Admin login page
    path('add-book/', views.add_book_page, name='add_book'),  # Add book page
    path('view-books/', views.view_books, name='view_book'),  # View all books
    path('update-book/<int:id>/submit/', views.update_book_submit, name='update_book_submit'),
    path('update-book/<int:id>/', views.update_book_page, name='update_book'),  # Update book page
    path('delete-book/<int:id>/', views.delete_book_page, name='delete_books'),  # Delete book page
    path('delete-book/<int:id>/confirm/', views.delete_book_submit, name='delete_book_submit'),


    # API Endpoints
    path('api/admin/signup/', views.admin_signup, name='api_signup'),
    path('api/admin/login/', views.admin_login, name='api_login'),
    path('api/add-book/', views.add_book, name='api_add_book'),
    path('api/get-books/', views.get_books, name='api_get_books'),
    path('api/update-book/<int:id>/', views.update_book, name='api_update_book'),
    path('api/delete-book/<int:id>/', views.delete_book, name='api_delete_book'),
]

