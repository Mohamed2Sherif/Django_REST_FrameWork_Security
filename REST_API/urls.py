from django.contrib import admin
from django.urls import path , include
from tickets.views import *
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token  
router = DefaultRouter()
router.register('guests',Viewsets_guest)
router.register('movies',Viewsets_movie)
router.register('reservation',Viewsets_reservation)
urlpatterns = [
    path('admin/', admin.site.urls),
    
    
    #1
    path("django/jsonresponsenomodel/",no_rest_no_model),
    #2
    path('django/jsonresponsefrommodel/',no_rest_from_model),
    #3 GET POST from rest framework function based view @api_view decorator
    path('rest/fbvlist',FBV_List),
    #4 GET PUT DELETE REST framework function based view @api_view decorator
    path('rest/fbvlist/<int:pk>',FBV_pk),
    #5 CBV LIST GET POST CLASS BASED VIEW APIView 
    path('rest/cbvlist',CBV_List.as_view()),
    path('rest/cbvlist/<int:pk>',CBV_pk.as_view()),
    
    #6 CBV LIST GET POST CLASS BASED VIEW and mixins
     path('rest/mixins/',mixins_list.as_view()),
    path('rest/mixins/<int:pk>/',mixins_pk.as_view()),
    

    # CBV LIST GET POST
    path('rest/generics/',generics_list.as_view()),
    path('rest/generics/<int:pk>/',generics_pk.as_view()),
    
    # Viewset LIST GET POST
    path('rest/viewsets/',include(router.urls)),
    
    
    #find movie 
    path('fbv/findmovie',find_movie),
    path('fbv/newreservation/',new_reservation),
    
    
    #auth
    path('api-auth',include('rest_framework.urls')),

    #Token Authentication 
    path('api-token-auth',obtain_auth_token),
    
    #Post_is_allowed_author 
    # path('post/generics/',Post_list.as_view()),
    path("Post/generics/<int:pk>",Post_pk.as_view())
]
