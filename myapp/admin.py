from django.contrib import admin

from myapp.models import *

admin.site.register(User)
admin.site.register(Vendor)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Shop)
admin.site.register(ShopReview)
admin.site.register(Product)
admin.site.register(ProductReview)
admin.site.register(Comment)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(Courier)
admin.site.register(VendorCourier)
admin.site.register(Driver)
admin.site.register(Follow)
admin.site.register(Coverage)
admin.site.register(CourierDriver)
