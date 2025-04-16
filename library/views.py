from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
import json
from .models import Admin, Book

# 👇 Homepage View to load the HTML template
def home(request):
    return render(request, 'library_front.html')  # This loads your homepage HTML

# 👇 Admin Signup View (for frontend form)
def admin_signup_page(request):
    if request.method == 'GET':
        return render(request, 'sign_up.html')  # Render signup form

    if request.method == 'POST':
        # Handle form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if Admin.objects.filter(email=email).exists():
            return JsonResponse({'message': 'Email already registered'}, status=400)
        
        admin = Admin(name=name, email=email, password=password)
        admin.save()
        return redirect('login')  # Redirect to login page after successful signup

# 👇 Admin Login View (for frontend form)
def admin_login_page(request):
    if request.method == 'GET':
        return render(request, 'login.html')  # Render login form

    if request.method == 'POST':
        # Handle form submission
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            admin = Admin.objects.get(email=email, password=password)
            return redirect('add_book')  # Redirect to Add Book page after login
        except Admin.DoesNotExist:
            return JsonResponse({'message': 'Invalid credentials'}, status=400)

# 👇 Add Book View (for frontend form)
def add_book_page(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        published_year = request.POST['published_year']
        isbn = request.POST['isbn']
        
        # Create the new book record
        Book.objects.create(title=title, author=author, published_year=published_year, isbn=isbn)
        
        # Redirect to the page that lists books
        return redirect('view_book')  # This assumes you have a 'view_book' URL

    return render(request, 'add_book.html')
 # Redirect to View Books page after adding the book

# 👇 View All Books
def view_books(request):
    books = Book.objects.all()  # Get all books from the database
    return render(request, 'view_book.html', {'books': books})

# 👇 Update Book View
def update_book_page(request, id):
    book = Book.objects.get(id=id)

    if request.method == 'GET':
        return render(request, 'update_book.html', {'book': book})

    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        published_year = request.POST.get('published_year')
        isbn = request.POST.get('isbn')

        book.title = title
        book.author = author
        book.published_year = published_year
        book.isbn = isbn
        book.save()
        return redirect('view_books')  # Redirect to View Books page after updating

# 👇 Delete Book View
def delete_book_page(request, id):
    book = Book.objects.get(id=id)

    if request.method == 'GET':
        return render(request, 'delete_books.html', {'book': book})

    if request.method == 'POST':
        book.delete()  # Delete the book from the database
        return redirect('view_books')  # Redirect to View Books page after deletion

# 👇 Admin Signup API
@csrf_exempt
def admin_signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if Admin.objects.filter(email=data['email']).exists():
            return JsonResponse({'message': 'Email already registered'}, status=400)
        admin = Admin(name=data['name'], email=data['email'], password=data['password'])
        admin.save()
        return JsonResponse({'message': 'Admin registered successfully'})

# 👇 Admin Login API
@csrf_exempt
def admin_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            admin = Admin.objects.get(email=data['email'], password=data['password'])
            return JsonResponse({'message': 'Login successful'})
        except Admin.DoesNotExist:
            return JsonResponse({'message': 'Invalid credentials'}, status=400)

# 👇 Add Book API
@csrf_exempt
def add_book(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        book = Book(title=data['title'], author=data['author'], published_year=data['published_year'], isbn=data['isbn'])
        book.save()
        return JsonResponse({'message': 'Book added successfully'})

# 👇 Get All Books API
def get_books(request):
    if request.method == 'GET':
        books = list(Book.objects.values())
        return JsonResponse(books, safe=False)

# 👇 Update Book API
@csrf_exempt
def update_book(request, id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            book = Book.objects.get(id=id)
            book.title = data['title']
            book.author = data['author']
            book.published_year = data['published_year']
            book.isbn = data['isbn']
            book.save()
            return JsonResponse({'message': 'Book updated successfully'})
        except Book.DoesNotExist:
            return JsonResponse({'message': 'Book not found'}, status=404)

# 👇 Delete Book API
@csrf_exempt
def delete_book(request, id):
    if request.method == 'DELETE':
        try:
            book = Book.objects.get(id=id)
            book.delete()
            return JsonResponse({'message': 'Book deleted successfully'})
        except Book.DoesNotExist:
            return JsonResponse({'message': 'Book not found'}, status=404)



@csrf_exempt
def update_book_submit(request, id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=id)
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.published_year = request.POST.get('published_year')
        book.isbn = request.POST.get('isbn')
        book.save()
        return redirect('view_book')
    return redirect('update_book', id=id)

@csrf_exempt
def delete_book_submit(request, id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=id)
        book.delete()
        return redirect('view_book')
    return redirect('delete_books', id=id)
