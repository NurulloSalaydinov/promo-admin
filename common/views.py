import json

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth.views import LoginView

from clients.models import Client, Order

from .models import Category, Promo, Product
from .forms import CategoryForm, PromoForm, ProductForm
from .utils import generate_promo



class UserLoginView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        return redirect('/')

    def form_invalid(self, form):
        messages.error(self.request,"Nato'gri username yoki parol")
        return self.render_to_response(self.get_context_data(form=form))

@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    category_count = Category.objects.all().count()
    product_count = Product.objects.all().count()
    client_count = Client.objects.all().count()
    orders = Order.objects.select_related('client', 'product').all()
    q = request.GET.get('q', None)
    sort = request.GET.get('sort', None)
    if q:
        orders = Order.objects.select_related('client', 'product').filter(Q(client__first_name__icontains=q) | Q(client__last_name__icontains=q) | Q(client__username__icontains=q) | Q(client__phone__icontains=q))
    if sort:
        if sort == 'all':
            orders = Order.objects.select_related('client', 'product').all()
        if sort == 'delivered':
            orders = Order.objects.select_related('client', 'product').filter(delivered=True)
        if sort == 'pending':
            orders = Order.objects.select_related('client', 'product').filter(delivered=False)
    context = {
        'category_count': category_count,
        'product_count': product_count,
        'client_count': client_count,
        'orders': orders
    }
    return render(request, 'dashboard.html', context)


# ALL About Category
@user_passes_test(lambda u: u.is_superuser)
def category(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'category/category.html', context)

@user_passes_test(lambda u: u.is_superuser)
def category_form(request):
    form = CategoryForm()
    if request.methodd == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Kategoriya qo'shildi")
            return redirect('dashboard:category')
    context = {'form': form}
    return render(request, 'category/category_form.html', context)

@user_passes_test(lambda u: u.is_superuser)
def category_update_form(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.info(request, "Kategoriya tahrirlandi")
            return redirect('dashboard:category')
    context = {'form': form, 'object': category}
    return render(request, 'category/category_form.html', context)

@user_passes_test(lambda u: u.is_superuser)
def category_delete_form(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        try:
            category.delete()
            messages.info(request, "Kategoriya o'chirildi")
        except:
            messages.warning(request, "Kategoriya o'chirilmadi")
        return redirect('dashboard:category')
    return render(request, 'delete.html', {'obj': category})

# ALL About Product
@user_passes_test(lambda u: u.is_superuser)
def product(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'product/product.html', context)

@user_passes_test(lambda u: u.is_superuser)
def product_form(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Sovg'a qo'shildi")
            return redirect('dashboard:product')
    context = {'form': form}
    return render(request, 'product/product_form.html', context)

@user_passes_test(lambda u: u.is_superuser)
def product_update_form(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.info(request, "Sovg'a tahrirlandi")
            return redirect('dashboard:product')
    context = {'form': form, 'object': product}
    return render(request, 'product/product_form.html', context)

@user_passes_test(lambda u: u.is_superuser)
def product_delete_form(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        try:
            product.delete()
            messages.info(request, "Produkt o'chirildi")
        except:
            messages.warning(request, "Produkt o'chirilmadi")
        return redirect('dashboard:product')
    return render(request, 'delete.html', {'obj': product})

# ALL About Promo
@user_passes_test(lambda u: u.is_superuser)
def promo(request):
    promos = Promo.objects.select_related('category').order_by('-id')
    paginator = Paginator(promos, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'promos': page_obj
    }
    return render(request, 'promo/promo.html', context)

@user_passes_test(lambda u: u.is_superuser)
def promo_form(request):
    categories = Category.objects.all()
    promocode_list = []
    errors = []
    if request.method == 'POST':
        cat = request.POST.get('category', None)
        count = request.POST.get('count', None)
        count = int(count)
        data = [cat, count]
        if data and count > 0:
            try:
                category = Category.objects.get(id=cat)
                for c in range(0, count):
                    code = generate_promo()
                    promocode_list.append(code)
                    Promo.objects.create(category=category, promocode=code)
                messages.info(request, "Promokod qo'shildi")
                return redirect(f'/promo-print?promos=%s' % json.dumps(promocode_list))
                # return render(request, 'pdf.html', context={'codes': promocode_list})
            except Exception as e:
                print(e)
                errors.append("Ma'lumotlar nato'gri kiritilgan.")
            return redirect('dashboard:promo')
        else:
            errors.append("Ma'lumotlar nato'gri kiritilgan.")
            return redirect('dashboard:promo')
    context = {'categories': categories}
    return render(request, 'promo/promo_form.html', context)

@user_passes_test(lambda u: u.is_superuser)
def promo_print(request):
    promos = request.GET.get('promos', None)
    if promos:
        promos = json.loads(promos)
        print('promos', promos)
        for p in promos:
            print('P', p)
        context = {
            'codes': promos
        }
        return render(request, 'pdf.html', context)
    return redirect('dashboard:promo')

@user_passes_test(lambda u: u.is_superuser)
def promo_delete_form(request, promo_id):
    promo = get_object_or_404(Promo, id=promo_id)
    if request.method == 'POST':
        try:
            promo.delete()
            messages.info(request, "Promokod o'chirildi")
        except:
            messages.warning(request, "Promokod o'chirilmadi")
        return redirect('dashboard:promo')
    return render(request, 'delete.html', {'obj': promo})

@user_passes_test(lambda u: u.is_superuser)
def promo_delete_date(request):
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)
    context = {}
    if start and end:
        promos = Promo.objects.select_related('category').filter(created_at__gte=start, created_at__lte=end)[:50]
        context['promos'] = promos
        context['count'] = Promo.objects.select_related('category').filter(created_at__gte=start, created_at__lte=end).count()
        if request.method == 'POST':
            try:
                promo_list = Promo.objects.filter(created_at__gte=start, created_at__lte=end)
                for promo in promo_list:
                    promo.delete()
                messages.info(request, "Promokod o'chirildi")
            except:
                messages.warning(request, "Promokod o'chirilmadi")
            return redirect('dashboard:promo')
    return render(request, 'promo/promo_delete.html', context)
