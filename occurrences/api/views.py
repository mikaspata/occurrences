from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework.permissions import IsAdminUser

from django.shortcuts import get_object_or_404
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.contrib.gis.geoip2 import GeoIP2

from api.models import Occurence
from api.serializers import OccurenceSerializer
 
 
class OccurenceView(APIView):
    def get(self, request):
        queryset = Occurence.objects.all()

        author = self.request.query_params.get('author', None)
        if author is not None:
            queryset = queryset.filter(author__icontains=author)

        occurence_category = self.request.query_params.get('occurence_category', None)
        if occurence_category is not None:
            queryset = queryset.filter(occurence_category__label__icontains=occurence_category)

        lat = self.request.query_params.get('latitude', None)
        lng = self.request.query_params.get('longitude', None)
        radius = self.request.query_params.get('radius', None)
        if lat is not None and lng is not None and radius is not None:
            queryset = queryset.filter(geo_location__distance_lt=(Point(float(lat), float(lng)), 
                                                                  Distance(km=radius)))

        serializer = OccurenceSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        ip = request.META.get('REMOTE_ADDR', None)
        if ip:
            try:
                g = GeoIP2()
                request.data['geo_location'] = str(Point(g.lat_lon(ip)))
            except:
                pass

        if request.user.is_authenticated():
            request.data['author_id'] = request.user.id

        serializer = OccurenceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            occurence_saved = serializer.save()
        
        return Response({
            "success": "Occurence '{}' created successfully".format(occurence_saved.description)
        })


class OccurenceDetail(APIView):
    permission_classes = (IsAdminUser,)

    def put(self, request, pk):
        occurence_saved = get_object_or_404(Occurence.objects.all(), pk=pk)
        serializer = OccurenceSerializer(instance=occurence_saved, 
                                         data=request.data, 
                                         partial=True)
        if serializer.is_valid(raise_exception=True):
            occurence_saved = serializer.save()
        
        return Response({
            "success": "Occurence '{}' updated successfully".format(occurence_saved.description)
        })

