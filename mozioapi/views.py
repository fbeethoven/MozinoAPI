# REST API FRAMEWORK
from rest_framework.decorators import api_view
from rest_framework.response import Response

# POLYGON and Point for GEOjson
from django.contrib.gis.geos import Polygon, Point

from .models import provider, area
from .serializers import providerSerializer, areaSerializer
    
#This is a heroku test

# ----------------------------------
#  Documenting the API endpoints by hand
# ----------------------------------
@api_view(['GET'])
def MozioAPIDoc(request):
    api_doc = [{
        'Endpoint' : '/api/get/all',
        'method' : 'GET',
        'body' : None ,
        'description' : 'Returns all Providers in the database'
        },
        {
        'Endpoint' : '/api/get/id',
        'method' : 'GET',
        'body' : None ,
        'description' : 'Returns the one Provider with the passed id'
        },
        {
        'Endpoint' : '/api/get/create',
        'method' : 'POST',
        'body' : {
            "name": "name",
            "email": "email@gmail.com",
            "phone_number": "+48 123 234 234",
            "language": "language",
            "currency": "USD"
            } ,
        'description' : 'Create a new Provider'
        },
        {
        'Endpoint' : '/api/id/update',
        'method' : 'PUT',
        'body' : {
            "name": "updatedname",
            "email": "updatedemail@gmail.com",
            "phone_number": "+48 123 234 234",
            "language": "language",
            "currency": "USD"
            } ,
        'description' : 'Update information about a Provider on the Database'
        },
        {
        'Endpoint' : '/api/get/delete',
        'method' : 'DELETE',
        'body' : None ,
        'description' : 'Deletes a Provider from the Database'
        },
        {
        'Endpoint' : '/api/id/polygon/all',
        'method' : 'GET',
        'body' : None ,
        'description' : 'Returns all Service Areas that a Provider has in the Database'
        },
        {
        'Endpoint' : '/api/id/polygon/pk',
        'method' : 'GET',
        'body' : None ,
        'description' : 'Returns on Service Area created by a Provider'
        },
        {
        'Endpoint' : '/api/id/polygon/create',
        'method' : 'POST',
        'body' : {
            "name" : "name of Service Area",
            "price" : "Price in the currency of the provider",
            "area" :  "geojson of the Polygon. Can easily be obtain in geojson.io for e.g."},
        'description' : 'Creates a new Service Area by the Provider with passed id'
        },
        {
        'Endpoint' : '/api/id/polygon/pk/update',
        'method' : 'PUT',
        'body' : {
            "name" : "name of Service Area",
            "price" : "Price in the currency of the provider",
            "area" :  "geojson of the Polygon. Can easily be obtain in geojson.io for e.g."
            } ,
        'description' : 'Updates a Service Area already on the Database'
        },
        {
        'Endpoint' : '/api/id/polygon/pk/delete',
        'method' : 'DELETE',
        'body' : None ,
        'description' : 'Deteles a Service Area from the Database'
        },
        {
        'Endpoint' : '/api/query?lat=000000&lng=00000',
        'method' : 'GET',
        'body' : None ,
        'description' : 'Returns all Service Areas that contain the Point of latitude and longitud specified'
        }
        ]
    return Response(api_doc)

# ----------------------------------
# END POINTS FOR PROVIDERS:
# ----------------------------------

@api_view(['GET'])
def getProvider(request, pk):
    provider_ = provider.objects.get(id=pk)
    serializer = providerSerializer(provider_, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getListProvider(request):
    provider_ = provider.objects.all()
    serializer = providerSerializer(provider_, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createProvider(request):
    provider_ = provider.objects.create(
        name = request.data['name'],
        email = request.data['email'],
        phone_number = request.data['phone_number'],
        language = request.data['language'],
        currency = request.data['currency'])
    serializer = providerSerializer(provider_, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def updateProvider(request, pk):
    provider_ = provider.objects.get(id=pk)
    serializer = providerSerializer(provider_, data = request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteProvider(request, pk):
    provider_ = provider.objects.get(id = pk)
    provider_.delete()
    return Response("Provider was deleted")




# ----------------------------------
# END POINTS FOR THE POLYGONS:
# ----------------------------------

@api_view(['GET'])
def getArea(request,id, pk): # The id will be used for authentication (only authenticated provider can see the polygons)
    area_ = area.objects.get(id=pk)
    serializer = areaSerializer(area_, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getListArea(request, id):
    provider_ = provider.objects.get(id=id)
    area_ = area.objects.filter(provider=provider_)
    serializer = areaSerializer(area_, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def createArea(request, id):
    provider_ = provider.objects.get(id=id)
    if len(request.data['area']['coordinates'])==1:
        polygon = Polygon(
            request.data['area']['coordinates'][0],[])
    elif len(request.data['area']['coordinates'])==2: 
        polygon = Polygon(
            request.data['area']['coordinates'][0],
            request.data['area']['coordinates'][1])
    else:
        return Response("Bad geojson data")
    area_ = area.objects.create(
        name = request.data['name'],
        price = request.data['price'],
        provider = provider_,
        service_area = polygon)
    serializer = areaSerializer(area_, many=False)
    return Response(serializer.data)



@api_view(['PUT'])
def updateArea(request,id, pk):
    provider_ = provider.objects.get(id=id)
    area_ = area.objects.filter(provider=provider_, id=pk)
    serializer = areaSerializer(area_, data = request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteArea(request,id, pk):
    provider_ = provider.objects.get(id = id)
    area_ = area.objects.filter(provider = provider_, id=pk)
    area_.delete()
    return Response("Area was deleted")


# ----------------------------------
# QUERY THE POLYGONS:
# ----------------------------------

@api_view(['GET'])
def queryArea(request):
    lat = float(request.GET.get('lat', None))
    lng = float(request.GET.get('lng', None))
    if lat==None or lng == None:
        return Response("Bad Query")
    print(type(lat))
    point = Point(lat,lng)
    print(point)

    query_set = area.objects.filter(service_area__contains=point)
    serializer = areaSerializer(query_set, many=True)
    return Response(serializer.data)






