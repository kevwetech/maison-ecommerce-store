from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Category
from .forms import ProductCreateForm
from django.contrib.auth.decorators import login_required

def homepage(request):
    all_categories = Category.objects.all()
    home_categories = Category.objects.all()[:6]
    featured_products = Product.objects.all().order_by('-id')[:9]

    products = Product.objects.all()
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    context = {
        "products": products,
        "categories": all_categories,
        "home_categories": home_categories,
        "featured_products": featured_products,
    }

    return render(request, "products/index.html", context)


def categories_page(request):
    categories = Category.objects.all()
    return render(request, 'products/categories.html', {'categories': categories})

def products_page(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    total_count = products.count()

    # Search
    search = request.GET.get('search', '')
    if search:
        products = products.filter(name__icontains=search)

    # Category filter
    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category_id=category_id)

    # Price filter - only apply if explicitly set
    max_price = request.GET.get('max_price', '')
    if max_price:
        products = products.filter(price__lte=max_price)
    max_price = max_price or 2000

    return render(request, "products/products.html", {
        "products": products,
        "categories": categories,
        "selected_category": category_id,
        "search": search,
        "max_price": int(max_price),
        "total_count": total_count,
    })


def product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]
    images = list(product.images.all())
    
    # Include main image as first slide if exists
    return render(request, 'products/product_details.html', {
        'product': product,
        'related_products': related_products,
        'images': images,
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


