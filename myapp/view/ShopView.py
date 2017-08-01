from datetime import date, datetime

from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from myapp.models import Vendor, User, Shop, Product, SubCategory
from myapp.serializers import ShopPostSerializer, ShopGetSerializer, ProductGetSerializer, ProductPostSerializer


class ShopView(APIView):
    # get all shops
    def get(self, request, format=None):
        print("shopview")
        shop = Shop.objects.all()
        serializer = ShopGetSerializer(shop, many=True)
        return Response({"Shops": serializer.data})

    # create shop
    def post(self, request, format=None):
        request.data['createdAt'] = datetime.strptime('24052010', "%d%m%Y").date()
        request.data['modifiedAt'] = datetime.strptime('24052010', "%d%m%Y").date()
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
        request.data['createdAt'] = datetime.strptime('24052010', "%d%m%Y").date()
        request.data['modifiedAt'] = datetime.strptime('24052010', "%d%m%Y").date()
        request.data['shop'] = shop_id
        serializer = ProductPostSerializer(data=request.data)

        print("db#")
        serializer.subCategory = SubCategory.objects.get(id=request.data['subCategory'])
        if serializer.is_valid():
            serializer.save()
            return Response({"Shops": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
