from django.conf.urls import url
from django.contrib import admin

from myapp import views
from myapp.view.ShopProductView import ShopProductView
from myapp.view.ShopView import ShopView, ShopDetailsView, ProductView
from myapp.view.UserView import UserView
from myapp.view.VendorView import VendorView, GetVendorShopsView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'api/v1/users$', UserView.as_view(), name='users'),
    url(r'api/v1/vendors$', VendorView.as_view(), name='vendors'),
    url(r'api/v1/vendors/(?P<vendor_id>[-\w]+)/shops$', GetVendorShopsView.as_view(), name='vendors-shops'),
    url(r'api/v1/shops/(?P<shop_id>[-\w]+)$', ShopDetailsView.as_view(), name='shop'),
    url(r'api/v1/shops', ShopView.as_view(), name='shops'),
    url(r'api/v1/shop_products/(?P<shop_id>[-\w]+)$', ShopProductView.as_view(), name='shop_product'),
    url(r'api/v1/products', ProductView.as_view(), name='products'),

]
