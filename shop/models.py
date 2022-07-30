from django.contrib.auth import get_user_model
from django.db import models, IntegrityError
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone

UserModel = get_user_model()


class CategoryModel(models.Model):
    name = models.CharField(max_length=60, verbose_name=_('name'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categoies')


class ProductBrandModel(models.Model):
    name = models.CharField(max_length=60, verbose_name=_('name'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('brand')
        verbose_name_plural = _('brands')


class ProductSizeModel(models.Model):
    name = models.CharField(max_length=60, verbose_name=_('name'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('size')
        verbose_name_plural = _('sizes')


class ProductColorModel(models.Model):
    code = models.CharField(max_length=60, verbose_name=_('code'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _('color')
        verbose_name_plural = _('colors')


class ProductTagModel(models.Model):
    name = models.CharField(max_length=60, verbose_name=_('name'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')


class ProductModel(models.Model):
    title = models.CharField(max_length=60, verbose_name=_('title'))
    short_description = models.CharField(max_length=255, verbose_name=_('short description'))
    long_description = RichTextUploadingField(verbose_name=_('long description'))
    price = models.FloatField(verbose_name=_('price'))
    real_price = models.FloatField(verbose_name=_('real price'), default=0)
    sale = models.BooleanField(default=False, verbose_name=_('sale'))
    discount = models.PositiveSmallIntegerField(default=0, verbose_name=_('discount'))
    main_image = models.ImageField(upload_to='products/', verbose_name=_('main image'))
    category = models.ForeignKey(
        CategoryModel,
        related_name='products',
        on_delete=models.RESTRICT,
        verbose_name=_('category')
    )
    tag = models.ManyToManyField(
        ProductTagModel,
        related_name='products',
        verbose_name=_('tag')
    )
    size = models.ManyToManyField(
        ProductSizeModel,
        related_name='products',
        verbose_name=_('sizes')
    )
    color = models.ManyToManyField(
        ProductColorModel,
        related_name='products',
        verbose_name=_('colors')
    )
    brand = models.ForeignKey(
        ProductBrandModel,
        on_delete=models.RESTRICT,
        related_name='products',
        verbose_name=_('brands'),
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))

    def is_discount(self):
        return bool(self.discount)

    def new(self):
        return (timezone.now() - self.created_at).days <= 5

    @staticmethod
    def get_cart_info(request):
        cart = request.session.get('cart', [])
        if not cart:
            return 0, 0.0
        return len(cart), ProductModel.objects.filter(id__in=cart).aggregate(Sum('real_price'))['real_price__sum']

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')


class WishlistModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name=_('wishlists'), verbose_name=_('user'))
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name=_('product'))

    @staticmethod
    def create_or_delete(user, product):
        try:
            return WishlistModel.objects.create(user=user, product=product)
        except IntegrityError:
            return WishlistModel.objects.get(user=user, product=product).delete()

    def __str__(self):
        return f"{self.user.get_full_name()} | {self.product.title}"

    class Meta:
        verbose_name = _('wishlist')
        verbose_name_plural = _('wishlists')
        unique_together = 'user', 'product'
