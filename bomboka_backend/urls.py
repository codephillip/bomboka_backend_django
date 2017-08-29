from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from bomboka_backend import settings
from myapp import views
from myapp.view.CourierView import CourierView, VendorCouriers, AllCoveragesListView, CourierCoveragesListView, \
    CourierCoveragesUpdateView, CourierDriversListView, CourierDriversDetailsView, CourierOrdersDetailsView, \
    VehicleView, \
    VehicleDetailsView, CourierVehicleListView, CourierVehicleDetailsView
from myapp.view.DriverView import DriversListView, DriverDetailsView, DriverEditView
from myapp.view.LocationView import CountryListView, CountryDetailsView
from myapp.view.OrderView import OrderDetailsView, OrdersListView, UserOrders
from myapp.view.ShopView import ShopView, ShopDetailsView, ProductView, ShopProductView, ShopEditView, ProductEditView, \
    ShopReviewView, ShopReviewDetailsView, ProductReviewsView, ProductReviewDetailsView, ShopFollowersView, \
    ShopFollowerDetailsView, ShopOrdersDetailsView, AttributeView, AttributeDetailsView, DiscountView, \
    DiscountDetailsView, BrandView, BrandDetailsView, ProductBrandView, ProductBrandDetailsView, SubscriptionView, \
    SubscriptionDetailsView
from myapp.view.UserView import UserCreateView, AddressView, UserAddressView, FollowedShopsView, UserOrdersDetailsView, \
    DisplayShopDiscounts, FeedbackCategoryView, FeedbackCategoryDetailsView, FeedbackDetailsView, FeedbackView, \
    UserLoginAPIView, UserView, UserDetailsView, ChangePasswordView
from myapp.view.VendorView import VendorView, GetVendorShopsView, VendorEditView, VendorOrdersDetailsView
"""
PLEASE FIRST TRY THE CURL TEST IN api_curl_tests.py BEFORE USING THE ENDPOINTS
"""
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # NOTE: this must be called first before accessing any endpoint
    # FOR DEBUGGING ONLY: activate 'AllowAny' in settings.py under DEFAULT_PERMISSION_CLASSES
    url(r'^api-token-auth', obtain_jwt_token),
    url(r'^api-token-refresh', refresh_jwt_token),
    url(r'^api-token-verify', verify_jwt_token),

    # password reset using email
    url('^', include('django.contrib.auth.urls')),
    url(r'accounts/login/$', views.successful_reset, name='register-user'),

    url(r'api/v1/users/register$', UserCreateView.as_view(), name='register-user'),
    url(r'api/v1/users/login$', UserLoginAPIView.as_view(), name='user-login'),
    url(r'api/v1/users/(?P<pk>[-\w]+)/reset_password$', ChangePasswordView.as_view(), name='change-user-password'),
    url(r'api/v1/users/(?P<user_id>[-\w]+)/addresses$', UserAddressView.as_view(), name='user_addresses'),
    url(r'api/v1/users/(?P<pk>[-\w]+)/orders', UserOrders.as_view(), name='user_orders'),
    url(r'api/v1/users/(?P<pk>[-\w]+)/followedShops', FollowedShopsView.as_view(), name='user-followed-shops'),
    url(r'api/v1/users/(?P<pk>[-\w]+)/orders$', UserOrdersDetailsView.as_view(),
        name='user-orders'),
    url(r'api/v1/users/(?P<pk>[-\w]+)/discounts$', DisplayShopDiscounts.as_view(),
        name='user-discounts'),
    url(r'api/v1/users$', UserView.as_view(), name='users'),
    url(r'api/v1/users/(?P<pk>[-\w]+)$', UserDetailsView.as_view(), name='user-details'),

    url(r'api/v1/feedbackcategorys$', FeedbackCategoryView.as_view(), name='feedback-categorys'),
    url(r'api/v1/feedbackcategorys/(?P<pk>[-\w]+)$', FeedbackCategoryDetailsView.as_view(),
        name='feedback-category-details'),
    url(r'api/v1/feedbacks$', FeedbackView.as_view(), name='feedbacks'),
    url(r'api/v1/feedbacks/(?P<pk>[-\w]+)$', FeedbackDetailsView.as_view(),
        name='feedback-details'),

    url(r'api/v1/addresses$', AddressView.as_view(), name='address'),

    url(r'api/v1/vendors$', VendorView.as_view(), name='vendors'),
    url(r'api/v1/vendors/(?P<vendor_id>[-\w]+)/shops$', GetVendorShopsView.as_view(), name='vendors_shops'),
    url(r'api/v1/vendors/(?P<vendor_id>[-\w]+)/couriers$', VendorCouriers.as_view(), name='vendors_couriers'),
    url(r'api/v1/vendor_edit/(?P<vendor_id>[-\w]+)$', VendorEditView.as_view(), name='edit_vendor'),
    url(r'api/v1/vendors/(?P<pk>[-\w]+)/orders$', VendorOrdersDetailsView.as_view(),
        name='vendor-orders'),

    url(r'api/v1/shops/(?P<shop_id>[-\w]+)$', ShopDetailsView.as_view(), name='shop-details'),
    url(r'api/v1/shops/(?P<pk>[-\w]+)/ratings$', ShopReviewView.as_view(), name='shop-ratings'),
    url(r'api/v1/shops/(?P<pk>[-\w]+)/ratings/(?P<pk2>[-\w]+)$', ShopReviewDetailsView.as_view(), name='shop-rating'),
    url(r'api/v1/shops/(?P<pk>[-\w]+)/followers$', ShopFollowersView.as_view(), name='shop-followers'),
    url(r'api/v1/shops/(?P<pk>[-\w]+)/followers/(?P<pk2>[-\w]+)$', ShopFollowerDetailsView.as_view(),
        name='shop-follower'),

    url(r'api/v1/products/(?P<pk>[-\w]+)/attributes$', AttributeView.as_view(), name='product-attributes'),
    url(r'api/v1/products/(?P<pk>[-\w]+)/attributes/(?P<pk2>[-\w]+)$', AttributeDetailsView.as_view(),
        name='product-attribute'),
    url(r'api/v1/products/(?P<pk>[-\w]+)/reviews/(?P<pk2>[-\w]+)$', ProductReviewDetailsView.as_view(),
        name='product-review'),
    url(r'api/v1/products/(?P<pk>[-\w]+)/reviews$', ProductReviewsView.as_view(), name='product-reviews'),
    url(r'api/v1/products$', ProductView.as_view(), name='products'),
    url(r'api/v1/product_edit/(?P<product_id>[-\w]+)$', ProductEditView.as_view(), name='edit_product'),
    url(r'api/v1/products/(?P<pk>[-\w]+)/brands$', ProductBrandView.as_view(), name='product-brand'),
    url(r'api/v1/products/(?P<pk>[-\w]+)/brands/(?P<pk2>[-\w]+)$', ProductBrandDetailsView.as_view(),
        name='product-brand'),

    url(r'api/v1/brands$', BrandView.as_view(), name='brands'),
    url(r'api/v1/brands/(?P<pk>[-\w]+)$', BrandDetailsView.as_view(), name='brand-details'),

    url(r'api/v1/discounts$', DiscountView.as_view(), name='discounts'),
    url(r'api/v1/discounts/(?P<pk>[-\w]+)$', DiscountDetailsView.as_view(), name='discount-details'),

    url(r'api/v1/shops$', ShopView.as_view(), name='shops'),
    url(r'api/v1/shop_edit/(?P<shop_id>[-\w]+)$', ShopEditView.as_view(), name='edit_shop'),
    url(r'api/v1/shops/(?P<shop_id>[-\w]+)/products$', ShopProductView.as_view(), name='shop_product'),
    url(r'api/v1/shops/(?P<pk>[-\w]+)/orders$', ShopOrdersDetailsView.as_view(),
        name='shop-orders'),

    url(r'api/v1/subscriptions$', SubscriptionView.as_view(), name='subscriptions'),
    url(r'api/v1/subscriptions/(?P<pk>[-\w]+)$', SubscriptionDetailsView.as_view(), name='subscription-details'),

    url(r'api/v1/orders$', OrdersListView.as_view(), name='orders'),
    url(r'api/v1/orders/(?P<pk>[-\w]+)$', OrderDetailsView.as_view(), name='order-details'),

    url(r'api/v1/drivers$', DriversListView.as_view(), name='drivers'),
    url(r'api/v1/drivers/(?P<pk>[-\w]+)$', DriverDetailsView.as_view(), name='driver-details'),
    url(r'api/v1/drivers_edit/(?P<pk>[-\w]+)$', DriverEditView.as_view(), name='edit-driver'),

    url(r'api/v1/coverages$', AllCoveragesListView.as_view(), name='courier-coverages'),

    url(r'api/v1/couriers$', CourierView.as_view(), name='couriers'),
    url(r'api/v1/couriers/(?P<pk>[-\w]+)/coverages$', CourierCoveragesListView.as_view(), name='courier-coverages'),
    url(r'api/v1/couriers/(?P<pk>[-\w]+)/coverages/(?P<pk2>[-\w]+)$', CourierCoveragesUpdateView.as_view(),
        name='courier-coverage'),
    url(r'api/v1/couriers/(?P<pk>[-\w]+)/drivers$', CourierDriversListView.as_view(),
        name='courier-drivers'),
    url(r'api/v1/couriers/(?P<pk>[-\w]+)/drivers/(?P<pk2>[-\w]+)$', CourierDriversDetailsView.as_view(),
        name='courier-driver'),
    url(r'api/v1/couriers/(?P<pk>[-\w]+)/orders$', CourierOrdersDetailsView.as_view(),
        name='courier-orders'),
    url(r'api/v1/couriers/(?P<pk>[-\w]+)/vehicles$', CourierVehicleListView.as_view(),
        name='courier-vehicles'),
    url(r'api/v1/couriers/(?P<pk>[-\w]+)/vehicles/(?P<pk2>[-\w]+)$', CourierVehicleDetailsView.as_view(),
        name='courier-vehicles'),
    url(r'api/v1/vehicles$', VehicleView.as_view(), name='vehicles'),
    url(r'api/v1/vehicles/(?P<pk>[-\w]+)$', VehicleDetailsView.as_view(), name='vehicle'),

    url(r'api/v1/countrys$', CountryListView.as_view(), name='countrys'),
    url(r'api/v1/countrys/(?P<pk>[-\w]+)$', CountryDetailsView.as_view(), name='country-details'),

]

urlpatterns += static(settings.MEDIA_ROOT, document_root=settings.MEDIA_ROOT)