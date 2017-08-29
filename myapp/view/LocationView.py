from myapp.models import Country
from myapp.serializers import CountrySerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class CountryListView(ListCreateAPIView):
    # Get all countrys / Create country
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CountryDetailsView(RetrieveUpdateDestroyAPIView):
    # Get one country / Delete country / Update country
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
