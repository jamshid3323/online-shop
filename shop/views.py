from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Min, Max
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import ProductModel, CategoryModel, ProductTagModel, ProductColorModel, ProductBrandModel, \
    ProductSizeModel, WishlistModel


class ShopView(ListView):
    template_name = 'shop.html'
    paginate_by = 3

    def get_queryset(self):
        qs = ProductModel.objects.all()
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(title__icontains=search)

        category = self.request.GET.get('cat')
        if category:
            qs = qs.filter(category_id=category)

        tag = self.request.GET.get('tag')
        if tag:
            qs = qs.filter(id=tag)

        brand = self.request.GET.get('brand')
        if brand:
            qs = qs.filter(brand=brand)

        size = self.request.GET.get('size')
        if size:
            qs = qs.filter(size=size)

        color = self.request.GET.get('color')
        if color:
            qs = qs.filter(color=color)

        sort = self.request.GET.get('sort')
        if sort == 'price':
            qs = qs.order_by('price')
        elif sort == '-price':
            qs = qs.order_by('-price')
        elif sort == 'sale':
            qs = qs.filter(sale=True)

        price = self.request.GET.get('price')
        if price:
            min, max = price.split(';')
            qs = qs.filter(real_price__gte=min, real_price__lte=max)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data()
        data['categories'] = CategoryModel.objects.all()
        data['tags'] = ProductTagModel.objects.all()
        data['brands'] = ProductBrandModel.objects.all()
        data['sizes'] = ProductSizeModel.objects.all()
        data['colors'] = ProductColorModel.objects.all()
        data['min_price'], data['max_price'] = ProductModel.objects.aggregate(Min('real_price'),
                                                                              Max('real_price')).values()

        return data


class ProductDetailView(DetailView):
    model = ProductModel
    template_name = 'shop-details.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data['products'] = ProductModel.objects.all().exclude(id=self.object.pk)[:4]

        return data


@login_required
def wishlist_view(request, pk):
    product = get_object_or_404(ProductModel, pk=pk)
    WishlistModel.create_or_delete(request.user, product)

    return redirect(request.GET.get('next', '/'))


class WishlistListView(LoginRequiredMixin, ListView):
    template_name = 'wishlist.html'

    def get_queryset(self):
        return ProductModel.objects.filter(wishlistmodel__user_id=self.request.user)


def update_cart_view(request, id):
    cart = request.session.get('cart', [])

    if id in cart:
        cart.remove(id)
    else:
        cart.append(id)

    request.session['cart'] = cart
    return redirect(request.GET.get('next', '/'))
