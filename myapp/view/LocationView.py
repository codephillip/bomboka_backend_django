from myapp.models import Country, City
from myapp.serializers import CountrySerializer, CityGetSerializer, CityPostSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class CountryListView(ListCreateAPIView):
    """
    Returns all countrys.
    Allows the admin to add country
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CountryDetailsView(RetrieveUpdateDestroyAPIView):
    """
    Allows RUD country
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityListView(ListCreateAPIView):
    """
    Returns all citys.
    Allows the admin to add city
    """
    queryset = City.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CityPostSerializer
        else:
            return CityGetSerializer


class CityDetailsView(RetrieveUpdateDestroyAPIView):
    """
    Allows RUD city
    """
    queryset = City.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return CityPostSerializer
        else:
            return CityGetSerializer
