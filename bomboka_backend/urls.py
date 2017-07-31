from django.conf.urls import url
from django.contrib import admin

from myapp import views
from myapp.view.ShopView import ShopView, ShopDetailsView
from myapp.view.UserView import UserView
from myapp.view.VendorView import VendorView, GetVendorShopsView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'api/v1/users$', UserView.as_view(), name='users'),
    url(r'api/v1/vendors$', VendorView.as_view(), name='vendors'),
    url(r'api/v1/vendors/(?P<vendor_id>[-\w]+)/shops$', GetVendorShopsView.as_view(), name='vendors-shops'),
    url(r'api/v1/shops/(?P<shop_id>[-\w]+)$', ShopDetailsView.as_view(), name='shopDetails'),
    url(r'api/v1/shops', ShopView.as_view(), name='shops'),
]
