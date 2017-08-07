from django.conf.urls import url
from django.contrib import admin

from myapp.view.CourierView import CourierView, VendorCouriers, AllCoveragesListView, CourierCoveragesListView, \
    CourierCoveragesUpdateView, CourierDriversListView, CourierDriversDetailsView
from myapp.view.DriverView import DriversListView, DriverDetailsView, DriverEditView
from myapp.view.OrderView import OrderDetailsView, OrdersListView, UserOrders
from myapp.view.ShopView import ShopView, ShopDetailsView, ProductView, ShopProductView, ShopEditView, ProductEditView, \
    ShopRatingsView, ShopRatingDetailsView, ProductReviewsView, ProductReviewDetailsView, ShopFollowersView, \
    ShopFollowerDetailsView
from myapp.view.UserView import UserView, AddressView, UserAddressView, FollowedShopsView
from myapp.view.VendorView import VendorView, GetVendorShopsView, VendorEditView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'api/v1/users$', UserView.as_view(), name='users'),
    url(r'api/v1/users/(?P<user_id>[-\w]+)/addresses$', UserAddressView.as_view(), name='user_addresses'),
    url(r'api/v1/users/(?P<pk>[-\w]+)/orders', UserOrders.as_view(), name='user_orders'),
    url(r'api/v1/users/(?P<pk>[-\w]+)/followedShops', FollowedShopsView.as_view(), name='user-followed-shops'),
    url(r'api/v1/vendors$', VendorView.as_view(), name='vendors'),
    url(r'api/v1/vendors/(?P<vendor_id>[-\w]+)/shops$', GetVendorShopsView.as_view(), name='vendors_shops'),
    url(r'api/v1/vendors/(?P<vendor_id>[-\w]+)/couriers$', VendorCouriers.as_view(), name='vendors_couriers'),
    url(r'api/v1/vendor_edit/(?P<vendor_id>[-\w]+)$', VendorEditView.as_view(), name='edit_vendor'),
    url(r'api/v1/shops/(?P<shop_id>[-\w]+)$', ShopDetailsView.as_view(), name='shop-details'),
    url(r'api/v1/shops/(?P<pk>[-\w]+)/ratings$', ShopRatingsView.as_view(), name='shop-ratings'),
    url(r'api/v1/shops/(?P<pk>[-\w]+)/ratings/(?P<pk2>[-\w]+)$', ShopRatingDetailsView.as_view(), name='shop-rating'),
    url(r'api/v1/shops/(?P<pk>[-\w]+)/followers$', ShopFollowersView.as_view(), name='shop-followers'),
    url(r'api/v1/shops/(?P<pk>[-\w]+)/followers/(?P<pk2>[-\w]+)$', ShopFollowerDetailsView.as_view(),
        name='shop-follower'),
    url(r'api/v1/products/(?P<pk>[-\w]+)/reviews$', ProductReviewsView.as_view(), name='product-reviews'),
    url(r'api/v1/products/(?P<pk>[-\w]+)/reviews/(?P<pk2>[-\w]+)$', ProductReviewDetailsView.as_view(),
        name='product-review'),
    url(r'api/v1/shop_edit/(?P<shop_id>[-\w]+)$', ShopEditView.as_view(), name='edit_shop'),
    url(r'api/v1/shops$', ShopView.as_view(), name='shops'),
    url(r'api/v1/shops/(?P<shop_id>[-\w]+)/products$', ShopProductView.as_view(), name='shop_product'),
    url(r'api/v1/products$', ProductView.as_view(), name='products'),
    url(r'api/v1/product_edit/(?P<product_id>[-\w]+)$', ProductEditView.as_view(), name='edit_product'),
    url(r'api/v1/addresses$', AddressView.as_view(), name='address'),
    url(r'api/v1/orders$', OrdersListView.as_view(), name='orders'),
    url(r'api/v1/orders/(?P<pk>[-\w]+)$', OrderDetailsView.as_view(), name='order-details'),
    url(r'api/v1/drivers$', DriversListView.as_view(), name='drivers'),
    url(r'api/v1/drivers/(?P<pk>[-\w]+)$', DriverDetailsView.as_view(), name='driver-details'),
    url(r'api/v1/drivers_edit/(?P<pk>[-\w]+)$', DriverEditView.as_view(), name='edit-driver'),
    url(r'api/v1/couriers$', CourierView.as_view(), name='couriers'),
    url(r'api/v1/coverages$', AllCoveragesListView.as_view(), name='courier-coverages'),
    url(r'api/v1/couriers/(?P<pk>[-\w]+)/coverages$', CourierCoveragesListView.as_view(), name='courier-coverages'),
    url(r'api/v1/couriers/(?P<pk>[-\w]+)/coverages/(?P<pk2>[-\w]+)$', CourierCoveragesUpdateView.as_view(),
        name='courier-coverage'),
    url(r'api/v1/couriers/(?P<pk>[-\w]+)/drivers$', CourierDriversListView.as_view(),
        name='courier-drivers'),
    url(r'api/v1/couriers/(?P<pk>[-\w]+)/drivers/(?P<pk2>[-\w]+)$', CourierDriversDetailsView.as_view(),
        name='courier-driver')
]
