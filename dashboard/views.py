from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from products.models import Product, Category
from orders.models import Order, OrderItem, DeliveryOption
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, F
from django.core.mail import send_mail


def admin_required(view_func):
    decorated = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url='login'
    )(view_func)
    return decorated


@admin_required
def dashboard_home(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(completed=False).count()
    low_stock_count = Product.objects.filter(stock__lte=5).count()
    total_revenue = OrderItem.objects.aggregate(
        revenue=Sum(F('price') * F('quantity'))
    )['revenue'] or 0
    recent_orders = Order.objects.order_by('-created_at')[:5]

    for order in recent_orders:
        order.total = order.items.aggregate(
            t=Sum(F('price') * F('quantity'))
        )['t'] or 0

    return render(request, 'dashboard/home.html', {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'low_stock_count': low_stock_count,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
    })


@admin_required
def product_list(request):
    query = request.GET.get('q', '')
    products = Product.objects.all()
    if query:
        products = products.filter(name__icontains=query) | products.filter(category__name__icontains=query)
    return render(request, 'dashboard/product_list.html', {'products': products, 'query': query})
    

@admin_required
def product_add(request):
    from products.forms import ProductCreateForm
    from products.models import ProductImage
    categories = Category.objects.all()
    form = ProductCreateForm()
    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            images = request.FILES.getlist('extra_images')
            print(f"Extra images received: {len(images)}")  # check terminal
            for img in images:
                ProductImage.objects.create(product=product, image=img)
            return redirect('dashboard_products')
    return render(request, 'products/product_form.html', {'form': form, 'categories': categories})


@admin_required
def product_edit(request, product_id):
    from products.forms import ProductCreateForm
    from products.models import ProductImage
    product = get_object_or_404(Product, pk=product_id)
    categories = Category.objects.all()
    form = ProductCreateForm(instance=product)
    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            # Save new extra images
            for img in request.FILES.getlist('extra_images'):
                ProductImage.objects.create(product=product, image=img)
            return redirect('dashboard_products')
    return render(request, 'products/product_update.html', {
        'form': form,
        'categories': categories,
        'product': product,
        'extra_images': product.images.all(),
    })


@admin_required
def delete_product_image(request, image_id):
    from products.models import ProductImage
    img = get_object_or_404(ProductImage, pk=image_id)
    product_id = img.product.id
    img.delete()
    return redirect('dashboard_product_edit', product_id=product_id)

@admin_required
def order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'dashboard/order_list.html', {'orders': orders})

@admin_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'dashboard/order_detail.html', {'order': order})

@admin_required
def order_update_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'processing', 'shipped', 'delivered']:
            order.status = new_status
            if new_status == 'delivered':
                order.completed = True
            order.save()

            # Send email to user
            status_messages = {
                'processing': 'Your order is being processed.',
                'shipped': 'Great news! Your order has been shipped and is on its way.',
                'delivered': 'Your order has been delivered. Thank you for shopping with us!',
                'pending': 'Your order status has been updated to pending.',
            }

            send_mail(
                subject=f'Order #{order.id} Status Update — {new_status.capitalize()}',
                message=f'Hi {order.full_name},\n\n{status_messages[new_status]}\n\nOrder #{order.id}\nStatus: {new_status.capitalize()}\n\nThank you for shopping with Maison!',
                from_email='noreply@maison.com',
                recipient_list=[order.email],
            )

            messages.success(request, f'Order status updated to {new_status}!')
    return redirect('dashboard_order_detail', order_id=order.id)

@admin_required
def category_list(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'dashboard/category_list.html', {'categories': categories})

@admin_required
def category_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        if name:
            Category.objects.create(name=name, image=image)
            messages.success(request, 'Category added successfully!')
            return redirect('dashboard_categories')
    return render(request, 'dashboard/category_form.html', {'action': 'Add'})



@admin_required
def category_edit(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        if name:
            category.name = name
            if image:
                category.image = image
            category.save()
            messages.success(request, 'Category updated!')
            return redirect('dashboard_categories')
    return render(request, 'dashboard/category_form.html', {'action': 'Edit', 'category': category})



@admin_required
def category_delete(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted.')
        return redirect('dashboard_categories')
    return render(request, 'dashboard/category_delete.html', {'category': category})



@admin_required
def delivery_options(request):
    options = DeliveryOption.objects.all()
    return render(request, 'dashboard/delivery_options.html', {'options': options})

@admin_required
def delivery_option_add(request):
    if request.method == 'POST':
        DeliveryOption.objects.create(
            name=request.POST.get('name'),
            delivery_type=request.POST.get('delivery_type'),
            price=request.POST.get('price'),
            estimated_days=request.POST.get('estimated_days'),
            free_above=request.POST.get('free_above') or None,
            is_active=request.POST.get('is_active') == 'on',
        )
        messages.success(request, 'Delivery option added!')
        return redirect('dashboard_delivery_options')
    return render(request, 'dashboard/delivery_option_form.html')

@admin_required
def delivery_option_edit(request, option_id):
    option = get_object_or_404(DeliveryOption, pk=option_id)
    if request.method == 'POST':
        option.name = request.POST.get('name')
        option.delivery_type = request.POST.get('delivery_type')
        option.price = request.POST.get('price')
        option.estimated_days = request.POST.get('estimated_days')
        option.free_above = request.POST.get('free_above') or None
        option.is_active = request.POST.get('is_active') == 'on'
        option.save()
        messages.success(request, 'Delivery option updated!')
        return redirect('dashboard_delivery_options')
    return render(request, 'dashboard/delivery_option_form.html', {'option': option})

@admin_required
def delivery_option_delete(request, option_id):
    option = get_object_or_404(DeliveryOption, pk=option_id)
    option.delete()
    messages.success(request, 'Delivery option deleted!')
    return redirect('dashboard_delivery_options')
