from datetime import datetime

from rest_framework.filters import OrderingFilter
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from rest_framework.response import Response
from rest_framework.views import APIView

from myapp.models import Vendor, Shop, Product, SubCategory, ShopReview, ProductReview, Follow, Order, Attribute, \
    Discount, Brand, ProductBrand, Subscription
from myapp.serializers import ShopPostSerializer, ShopGetSerializer, ProductGetSerializer, ProductPostSerializer, \
    ShopReviewGetSerializer, ShopReviewPostSerializer, ProductReviewPostSerializer, ProductReviewGetSerializer, \
    FollowPostSerializer, \
    FollowGetSerializer, OrderGetSerializer, AttributePostSerializer, AttributeGetSerializer, DiscountGetSerializer, \
    DiscountPostSerializer, BrandSerializer, ProductBrandPostSerializer, ProductBrandGetSerializer, \
    SubscriptionSerializer, VendorGetSerializer, FollowReportSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView, \
    RetrieveUpdateDestroyAPIView, ListAPIView, DestroyAPIView


class ShopView(ListAPIView):
    """
    Returns all shops in the System(Admin Only)
    """
    queryset = Shop.objects.all()
    serializer_class = ShopGetSerializer
    permission_classes = [IsAdminUser]


class ShopDetailsView(APIView):
    # get single shop details
    def get(self, request, shop_id):
        print(shop_id)
        shop = Shop.objects.filter(id=shop_id)
        serializer = ShopGetSerializer(shop, many=True)
        return Response({"Shops": serializer.data})


class ShopEditView(RetrieveUpdateAPIView):
    serializer_class = ShopPostSerializer

    # edit shop
    def put(self, request, *args, **kwargs):
        # post all the field when editing
        print("put##")
        print(kwargs['shop_id'])
        shop = Shop.objects.filter(id=kwargs['shop_id'])
        name = request.data['name']
        is_blocked = request.data['is_blocked']
        if name and is_blocked:
            shop.update(name=name, is_blocked=(is_blocked == "true"),
                        modifiedAt=datetime.strptime('24052010', "%d%m%Y").now())
        serializer = ShopGetSerializer(shop, many=True)
        return Response({"Shops": serializer.data})


class ProductView(ListAPIView):
    """
    Returns all products in the System(Admin Only)
    """
    queryset = Product.objects.all()
    serializer_class = ProductGetSerializer
    permission_classes = [IsAdminUser]


class ShopProductView(ListCreateAPIView):
    """
    Returns all Shop Products
    Allows User to add Product to Shop
    """
    def get_queryset(self):
        return Product.objects.filter(shop_id=self.kwargs['pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            self.request.POST._mutable = True
            try:
                self.request.data['shop'] = self.kwargs['pk']
            except Exception as e:
                print(e)
            return ProductPostSerializer
        else:
            return ProductGetSerializer


class ProductEditView(RetrieveUpdateAPIView):
    # edit product
    def put(self, request, *args, **kwargs):
        # post all the field when editing
        print("put##")
        product = Product.objects.filter(id=kwargs['product_id'])
        name = request.data['name']
        image = request.data['image']
        price = request.data['price']
        description = request.data['description']

        if product and name and image and price and description:
            product.update(name=name, image=image, price=price, description=description,
                           modifiedAt=datetime.strptime('24052010', "%d%m%Y").now())
            serializer = ProductGetSerializer(product, many=True)
            return Response({"Products": serializer.data})
        return Response("Failed to edit product", status=status.HTTP_400_BAD_REQUEST)


class ShopReviewView(ListCreateAPIView):
    """
    Returns all shop reviews
    Allows user to create shop review
    """
    def get_queryset(self):
        ratings = ShopReview.objects.filter(shop=self.kwargs['pk'])
        return ratings

    def get_serializer_class(self):
        if self.request.method == 'POST':
            self.request.POST._mutable = True
            try:
                self.request.data['shop'] = self.kwargs['pk']
            except Exception as e:
                print(e)
            return ShopReviewPostSerializer
        else:
            return ShopReviewGetSerializer


class ShopReviewDetailsView(RetrieveUpdateDestroyAPIView):
    """
    Returns single shop review
    Allows UD of shop review
    """
    # pk2->rating.id passed to the queryset
    lookup_url_kwarg = 'pk2'

    def get_queryset(self):
        ratings = ShopReview.objects.filter(shop=self.kwargs['pk'])
        return ratings

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ShopReviewPostSerializer
        else:
            return ShopReviewGetSerializer


class MostPopularShopsView(ListAPIView):
    """
    Returns most popular shops
    """
    serializer_class = ShopGetSerializer
    # filter_backends = (OrderingFilter,)
    # ordering_fields = ('count',)

    def get_queryset(self):
        # TODO FIX SERIOUS BUG
        shopReviews = ShopReview.objects.all().order_by('-shop__shopreview__count').distinct()
        print("Count# " + str(shopReviews.count()))
        count = 0
        for z in shopReviews:
            count += 1
            print(count)
        shops = [x.shop for x in shopReviews]
        return shops


class ProductReviewsView(ListCreateAPIView):
    """
    Returns all product reviews
    Allows user to create product review
    """
    def get_queryset(self):
        reviews = ProductReview.objects.filter(product=self.kwargs['pk'])
        return reviews

    def get_serializer_class(self):
        if self.request.method == 'POST':
            self.request.POST._mutable = True
            try:
                self.request.data['product'] = self.kwargs['pk']
            except Exception as e:
                print(e)
            return ProductReviewPostSerializer
        else:
            return ProductReviewGetSerializer


class ProductReviewDetailsView(RetrieveUpdateDestroyAPIView):
    """
    Returns single product review
    Allows UD of review
    """
    # pk2->review.id passed to the queryset
    lookup_url_kwarg = 'pk2'

    def get_queryset(self):
        reviews = ProductReview.objects.filter(product=self.kwargs['pk'])
        return reviews

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ProductReviewPostSerializer
        else:
            return ProductReviewGetSerializer


class AttributeView(ListCreateAPIView):
    def get_queryset(self):
        attribute = Attribute.objects.filter(product=self.kwargs['pk'])
        return attribute

    def get_serializer_class(self):
        if self.request.method == 'POST':
            self.request.POST._mutable = True
            try:
                self.request.data['product'] = self.kwargs['pk']
            except Exception as e:
                print(e)
            return AttributePostSerializer
        else:
            return AttributeGetSerializer


class AttributeDetailsView(RetrieveUpdateDestroyAPIView):
    # todo move into product
    # Get one product_attribute, Edit product_attribute, Delete product_attribute
    # pk2->attribute.id passed to the queryset
    lookup_url_kwarg = 'pk2'

    def get_queryset(self):
        attribute = Attribute.objects.filter(product=self.kwargs['pk'])
        return attribute

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            self.request.POST._mutable = True
            try:
                self.request.data['product'] = self.kwargs['pk']
            except Exception as e:
                print(e)
            return AttributePostSerializer
        else:
            return AttributeGetSerializer


class ShopFollowersView(ListCreateAPIView):
    """
    Returns all followers of the shop
    Allows user to follow shop
    """
    def get_queryset(self):
        follows = Follow.objects.filter(shop=self.kwargs['pk'])
        print(follows)
        return follows

    def get_serializer_class(self):
        if self.request.method == 'POST':
            # grab the url data then insert into the request dictionary
            try:
                self.request.data['shop'] = self.kwargs['pk']
            except Exception as e:
                print(e)
            return FollowPostSerializer
        else:
            return FollowGetSerializer


class ShopFollowerDetailsView(RetrieveDestroyAPIView):
    """
    Returns single shop follower
    Allows user unfollow shop
    """
    # pk2->stop.id passed to the queryset
    lookup_url_kwarg = 'pk2'

    def get_queryset(self):
        follows = Follow.objects.filter(shop=self.kwargs['pk'])
        return follows

    def get_serializer_class(self):
        return FollowGetSerializer


class ShopOrdersDetailsView(ListAPIView):
    """
    Returns all orders made from shop
    """
    serializer_class = OrderGetSerializer

    def get_queryset(self):
        return Order.objects.filter(product__shop=self.kwargs['pk'])


class DiscountView(ListCreateAPIView):
    """
    Returns all discounts.
    Allows creation of discount by the vendor.
    """
    queryset = Discount.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DiscountPostSerializer
        else:
            return DiscountGetSerializer


class DiscountDetailsView(RetrieveUpdateDestroyAPIView):
    """
    Returns single discount
    Allows deletion of discount
    """
    queryset = Discount.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return DiscountPostSerializer
        else:
            return DiscountGetSerializer


class BrandView(ListCreateAPIView):
    """
    Returns all brands.
    Allows admin to create brand.
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandDetailsView(RetrieveUpdateDestroyAPIView):
    """
    Allows RUD brand by admin.
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ProductBrandView(ListCreateAPIView):
    def get_queryset(self):
        return ProductBrand.objects.filter(product_id=self.kwargs['pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductBrandPostSerializer
        else:
            return ProductBrandGetSerializer


class ProductBrandDetailsView(RetrieveUpdateDestroyAPIView):
    # todo move brand into product model
    # Get one product_brand, Delete product_brand
    # pk2->brand.id passed to the queryset
    lookup_url_kwarg = 'pk2'

    def get_serializer_class(self):
        return ProductBrandPostSerializer

    def get_queryset(self):
        return ProductBrand.objects.filter(product_id=self.kwargs['pk'])


class SubscriptionView(ListCreateAPIView):
    """
    Returns all the subscriptions.
    Allows admin to create subscription.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class SubscriptionDetailsView(RetrieveUpdateDestroyAPIView):
    """
    Allows RUD subscription.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class ShopReportListView(APIView):
    def get(self, request, format=None):
        pass


class FollowersReportListView(ListAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowReportSerializer
