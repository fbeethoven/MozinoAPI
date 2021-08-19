from django.contrib import admin
from django.urls import path, include
from . import views
 
urlpatterns = [
    path('get/<int:pk>', views.getProvider, name="get_provider"),
    path('get/all', views.getListProvider,name="get_provider_list"),
    path('create', views.createProvider,name="create_provider"),
    path('<int:pk>/update', views.updateProvider,name="update_provider"),
    path('<int:pk>/delete', views.deleteProvider,name="delete_provider"),
    path('<int:id>/polygon/<int:pk>', views.getArea,name="get_polygon"),
    path('<int:id>/polygon/all', views.getListArea,name="get_polygon_list"),
    path('<int:id>/polygon/create', views.createArea,name="create_polygon"),
    path('<int:id>/polygon/<int:pk>/update', views.updateArea,name="update_polygon"),
    path('<int:id>/polygon/<int:pk>/delete', views.deleteArea,name="delete_polygon"),
    path('query', views.queryArea,name="query_polygon"),
]
