from django.conf.urls import url
from django.contrib import admin

from myapp import views
from myapp.view.ShopView import ShopView
from myapp.view.UserView import UserView
from myapp.view.VendorView import VendorView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'api/v1/users$', UserView.as_view(), name='users'),
    url(r'api/v1/vendors$', VendorView.as_view(), name='vendors'),
    url(r'api/v1/shops', ShopView.as_view(), name='shops'),
]
