from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import models as db_models
from .models import Product, Category, Wishlist, Review
from .forms import ProductCreateForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Avg


def homepage(request):
    all_categories = Category.objects.all()
    home_categories = Category.objects.all()[:6]
    featured_products = Product.objects.all().order_by('-id')[:8]
    wishlist_ids = []

    if request.user.is_authenticated:
        wishlist_ids = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))


    products = Product.objects.all()
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    context = {
        "products": products,
        "categories": all_categories,
        "home_categories": home_categories,
        "featured_products": featured_products,
        "wishlist_ids": wishlist_ids,
    }

    return render(request, "products/index.html", context)


def categories_page(request):
    categories = Category.objects.all()
    return render(request, 'products/categories.html', {'categories': categories})

def products_page(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    total_count = products.count()
    wishlist_ids = []

    if request.user.is_authenticated:
        wishlist_ids = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))

    # Search
    search = request.GET.get('search', '')
    if search:
        products = products.filter(name__icontains=search)

    # Category filter
    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category_id=category_id)

    # Price filter
    max_price = request.GET.get('max_price', '')
    if max_price:
        products = products.filter(price__lte=max_price)
    max_price = max_price or 1000000000

    return render(request, "products/products.html", {
        "products": products,
        "categories": categories,
        "selected_category": category_id,
        "search": search,
        "max_price": int(max_price),
        "total_count": total_count,
        "wishlist_ids": wishlist_ids,
    })


def product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]
    images = list(product.images.all())
    wishlist_ids = []
    reviews = product.reviews.all().order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    user_review = None

    if request.user.is_authenticated:
        wishlist_ids = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))
        user_review = reviews.filter(user=request.user).first()
    
    # Include main image as first slide if exists
    return render(request, 'products/product_details.html', {
        'product': product,
        'related_products': related_products,
        'images': images,
        'wishlist_ids': wishlist_ids,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'user_review': user_review,
    })

def product_create(request):
    if request.method == "POST":
        form = ProductCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # change later if needed
    else:
        form = ProductCreateForm()

    return render(request, 'products/product_form.html', {'form': form})



@login_required
def product_update(request, pk):
    # Get the product instance or return 404
    product = get_object_or_404(Product, pk=pk)

    # Bind the form to POST data and the instance
    form = ProductCreateForm(request.POST or None, request.FILES or None, instance=product)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('product_detail', pk=product.pk)  # redirect to product detail page
        else:
            messages.error(request, "Please correct the errors below.")

    return render(request, 'products/product_form.html', {'form': form, 'product': product})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('dashboard_products')
    return render(request, 'products/product_delete.html', {'product': product})


@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        wishlist_item.delete()
        return JsonResponse({'status': 'removed'})
    return JsonResponse({'status': 'added'})

@login_required
def wishlist_page(request):
    items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'products/wishlist.html', {'items': items})



@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if rating and comment:
            Review.objects.update_or_create(
                user=request.user,
                product=product,
                defaults={'rating': rating, 'comment': comment}
            )
            messages.success(request, 'Review submitted successfully!')
        else:
            messages.error(request, 'Please provide a rating and comment.')
    return redirect('product_details', product_id=product_id)




def about_page(request):
    return render(request, 'products/about.html')

def contact_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        send_mail(
            subject=f'Maison Contact: {subject}',
            message=f'From: {name} ({email})\n\n{message}',
            from_email=email,
            recipient_list=[os.environ.get('ADMIN_EMAIL')],
        )
        messages.success(request, 'Your message has been sent! We will get back to you soon.')
        return redirect('contact_page')
    return render(request, 'products/contact.html')