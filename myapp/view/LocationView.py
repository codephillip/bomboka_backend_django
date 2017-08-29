from myapp.models import Country, City
from myapp.serializers import CountrySerializer, CityGetSerializer, CityPostSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class CountryListView(ListCreateAPIView):
    # Get all countrys / Create country
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CountryDetailsView(RetrieveUpdateDestroyAPIView):
    # Get one country / Delete country / Update country
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityListView(ListCreateAPIView):
    # Get all citys / Create city
    queryset = City.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CityPostSerializer
        else:
            return CityGetSerializer


class CityDetailsView(RetrieveUpdateDestroyAPIView):
    # Get one city / Delete city / Update city
    queryset = City.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return CityPostSerializer
        else:
            return CityGetSerializer
