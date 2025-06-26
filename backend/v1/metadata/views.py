from django.core.cache import caches
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
# from admin_panel.models import CountryDetails

def demo(request):
    return HttpResponse("Other api is working")

class MetaDataViewSet(viewsets.ViewSet):
    @action(methods=['GET'], url_path='countrydetails', detail=False)
    def other_metadata_countrydetails(self, request):
        metadata_cached = caches['metadata']
        countries = metadata_cached.get("countries_data")
        if not countries:
            return JsonResponse({"error": "No country data found in cache"}, status=status.HTTP_404_NOT_FOUND)
        return JsonResponse({"countries": countries})
