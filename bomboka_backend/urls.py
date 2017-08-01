from django.conf.urls import url
from django.contrib import admin

from myapp.view.CourierView import CourierView, VendorCouriers
from myapp.view.OrderView import OrderView, UserOrders
from myapp.view.ShopView import ShopView, ShopDetailsView, ProductView, ShopProductView, ShopEditView
from myapp.view.UserView import UserView, AddressView, UserAddressView
from myapp.view.VendorView import VendorView, GetVendorShopsView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'api/v1/users$', UserView.as_view(), name='users'),
    url(r'api/v1/users/(?P<user_id>[-\w]+)/addresses$', UserAddressView.as_view(), name='user_addresses'),
    url(r'api/v1/users/(?P<user_id>[-\w]+)/orders', UserOrders.as_view(), name='user_orders'),
    url(r'api/v1/vendors$', VendorView.as_view(), name='vendors'),
    url(r'api/v1/vendors/(?P<vendor_id>[-\w]+)/shops$', GetVendorShopsView.as_view(), name='vendors_shops'),
    url(r'api/v1/vendors/(?P<vendor_id>[-\w]+)/couriers$', VendorCouriers.as_view(), name='vendors_couriers'),
    url(r'api/v1/shops/(?P<shop_id>[-\w]+)$', ShopDetailsView.as_view(), name='shop_details'),
    url(r'api/v1/shop_edit/(?P<shop_id>[-\w]+)$', ShopEditView.as_view(), name='edit_shop'),
    url(r'api/v1/shops$', ShopView.as_view(), name='shops'),
    url(r'api/v1/shops/(?P<shop_id>[-\w]+)/products$', ShopProductView.as_view(), name='shop_product'),
    url(r'api/v1/products$', ProductView.as_view(), name='products'),
    url(r'api/v1/addresses$', AddressView.as_view(), name='address'),
    url(r'api/v1/orders$', OrderView.as_view(), name='orders'),
    url(r'api/v1/couriers$', CourierView.as_view(), name='couriers'),

]
