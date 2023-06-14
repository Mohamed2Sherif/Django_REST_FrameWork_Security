from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Guest, Movie, Reservation
from rest_framework.decorators import api_view
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets, filters

# Create your views here.


# 1 without REST and no model qurey FBView
def no_rest_no_model(request):
    guests = [
        {"id": 1, "name": "omar", "mobile": 5456},
        {"id": 2, "name": "jsom", "mobile": 5426},
    ]  # i want to convert this data to json form
    return JsonResponse(guests, safe=False)


# 2 no_rest_from_model
def no_rest_from_model(request):
    data = Guest.objects.all()
    response = {"guests": list(data.values("Name", "mobile"))}

    return JsonResponse(response, safe=False)


# 3 Function based views
# 3.1 GET POST


@api_view(["GET", "POST"])
def FBV_List(request):
    # GET
    if request.method == "GET":
        guests = Guest.objects.all()
        seralizer = GuestSerializer(guests, many=True)
        return Response(seralizer.data)

    # POST
    elif request.method == "POST":
        seralizer = GuestSerializer(data=request.data)
        if seralizer.is_valid():
            seralizer.save()
            return Response(seralizer.data, status=status.HTTP_201_CREATED)
        return Response(seralizer.errors, status=status.HTTP_400_BAD_REQUEST)


# 3.2 GET PUT DELETE
@api_view(["GET", "PUT", "DELETE"])
def FBV_pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        seralizer = GuestSerializer(guest)
        return Response(seralizer.data)
    elif request.method == "PUT":
        seralizer = GuestSerializer(guest, data=request.data)
        if seralizer.is_valid():
            seralizer.save()
            return Response(seralizer.data)
        return Response(seralizer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# CBV
# 4.1 List and create == GET and POST


class CBV_List(APIView):
    def get(self, request, *args, **kwargs):
        guests = Guest.objects.all()
        seralizer = GuestSerializer(guests, many=True)
        return Response(seralizer.data)

    def post(self, request, *args, **kwargs):
        seralizer = GuestSerializer(data=request.data)
        if seralizer.is_valid():
            seralizer.save()
            return Response(seralizer.data, status=status.HTTP_201_CREATED)
        return Response(seralizer.errors, status=status.HTTP_400_BAD_REQUEST)


# 4.2 List and update == GET and PUT and DELETE
class CBV_pk(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)

        except Guest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        guest = self.get_object(pk)
        seralizer = GuestSerializer(guest)
        return Response(seralizer.data)

    def put(self, request, pk):
        guest = self.get_object(pk)
        seralizer = GuestSerializer(guest, data=request.data)
        if seralizer.is_valid():
            seralizer.save()
            return Response(seralizer.data)
        return Response(seralizer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 5
# 5.1


class mixins_list(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


# 5.2


class mixins_pk(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def put(self, request, pk):
        return self.update(request, pk)

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)


# 6 Generics
# 6.1
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


# 6.2
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


# 7 View Sets
class Viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class Viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backend = [filters.SearchFilter]
    search_fields = ["movie", "hall"]


class Viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


# 8 Find Movie
@api_view(["GET"])
def find_movie(request):
    
    movies = Movie.objects.filter(
        hall=request.data['hall'],
        movie=request.data["movie"],
    )
    seriazlier = MovieSerializer(movies, many=True)
    return Response(seriazlier.data,status=status.HTTP_200_OK)


# 9 create new reservation object


@api_view(["POST"])
def new_reservation(request):
    movie = Movie.objects.get(hall=request.data["hall"], movie=request.data["movie"])
    
    
    
    try: 
        guest = Guest.objects.get(Name= request.data["name"], mobile=request.data["mobile"])
    except Guest.DoesNotExist:
        guest = Guest()
        guest.Name = request.data["name"]
        guest.mobile = request.data["mobile"]
        guest.save()

    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()
    serializer = ReservationSerializer(reservation)
    return Response(serializer.data,status=status.HTTP_201_CREATED)
