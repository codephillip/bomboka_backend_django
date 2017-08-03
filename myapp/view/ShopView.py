from datetime import date, datetime, timezone

from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from myapp.models import Vendor, User, Shop, Product, SubCategory, Rating, Review, Follow
from myapp.serializers import ShopPostSerializer, ShopGetSerializer, ProductGetSerializer, ProductPostSerializer, \
    RatingGetSerializer, RatingPostSerializer, ReviewPostSerializer, ReviewGetSerializer, FollowPostSerializer, \
    FollowGetSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView, \
    RetrieveUpdateDestroyAPIView


class ShopView(APIView):
    # get all shops
    def get(self, request, format=None):
        print("shopview")
        shop = Shop.objects.all()
        serializer = ShopGetSerializer(shop, many=True)
        return Response({"Shops": serializer.data})

    # create shop
    def post(self, request, format=None):
        request.data['createdAt'] = datetime.strptime('24052010', "%d%m%Y").now()
        request.data['modifiedAt'] = datetime.strptime('24052010', "%d%m%Y").now()
        serializer = ShopPostSerializer(data=request.data)

        print("db#")
        print(Vendor.objects.get(id=request.data['vendor']))
        serializer.vendor = Vendor.objects.get(id=request.data['vendor'])
        if serializer.is_valid():
            serializer.save()
            return Response({"Shops": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopDetailsView(APIView):
    # get single shop details
    def get(self, request, shop_id):
        print(shop_id)
        shop = Shop.objects.filter(id=shop_id)
        serializer = ShopGetSerializer(shop, many=True)
        return Response({"Shops": serializer.data})


class ShopEditView(RetrieveUpdateAPIView):
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


class ProductView(APIView):
    # get all products
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductGetSerializer(products, many=True)
        return Response({"Products": serializer.data})


class ShopProductView(APIView):
    # get shop products
    def get(self, request, shop_id):
        print("shopproducts##")
        products = Product.objects.filter(shop_id=shop_id)
        serializer = ProductGetSerializer(products, many=True)
        return Response({"Products": serializer.data})

    # add product to shop
    def post(self, request, shop_id):
        print("post product##")
        request.data['createdAt'] = datetime.strptime('24052010', "%d%m%Y").now()
        request.data['modifiedAt'] = datetime.strptime('24052010', "%d%m%Y").now()
        request.data['shop'] = shop_id
        serializer = ProductPostSerializer(data=request.data)

        print("db#")
        serializer.subCategory = SubCategory.objects.get(id=request.data['subCategory'])
        if serializer.is_valid():
            serializer.save()
            return Response({"Shops": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class ShopRatingsView(ListCreateAPIView):
    # Get all shop ratings / Create shop rating
    def get_queryset(self):
        ratings = Rating.objects.filter(shop=self.kwargs['pk'])
        return ratings

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RatingPostSerializer
        else:
            return RatingGetSerializer


class ShopRatingDetailsView(RetrieveUpdateDestroyAPIView):
    # Get one shop_rating, Edit shop_rating, Delete shop_rating
    # pk2->rating.id passed to the queryset
    lookup_url_kwarg = 'pk2'

    def get_queryset(self):
        ratings = Rating.objects.filter(shop=self.kwargs['pk'])
        return ratings

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return RatingPostSerializer
        else:
            return RatingGetSerializer


class ProductReviewsView(ListCreateAPIView):
    # Get all product reviews / Create product review
    def get_queryset(self):
        reviews = Review.objects.filter(product=self.kwargs['pk'])
        return reviews

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewPostSerializer
        else:
            return ReviewGetSerializer


class ProductReviewDetailsView(RetrieveUpdateDestroyAPIView):
    # Get one product_review, Edit product_review, Delete product_review
    # pk2->review.id passed to the queryset
    lookup_url_kwarg = 'pk2'

    def get_queryset(self):
        reviews = Review.objects.filter(product=self.kwargs['pk'])
        return reviews

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ReviewPostSerializer
        else:
            return ReviewGetSerializer


class ShopFollowersView(ListCreateAPIView):
    # Get all user_followed_shops / Follow shop
    print("follow get###")

    def get_queryset(self):
        follows = Follow.objects.filter(shop=self.kwargs['pk'])
        print(follows)
        return follows

    def get_serializer_class(self):
        if self.request.method == 'POST':
            # grab the url data then insert into the request dictionary
            self.request.data['shop'] = self.kwargs['pk']
            return FollowPostSerializer
        else:
            return FollowGetSerializer


class ShopFollowerDetailsView(RetrieveDestroyAPIView):
    # Get one followed shop, Edit follow, Unfollow shop
    # pk2->stop.id passed to the queryset
    lookup_url_kwarg = 'pk2'

    def get_queryset(self):
        follows = Follow.objects.filter(shop=self.kwargs['pk'])
        return follows

    def get_serializer_class(self):
        return FollowGetSerializer
