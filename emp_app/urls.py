from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='index'),
    path('all_empolyee', views.allempolyee, name='allempolyee'),
    path('add_empolyee', views.add_empolyee, name='add_empolyee'),
    path('del_emp', views.del_emp, name='del_emp'),
    path('filter_emp', views.filter_emp, name='filter_emp')

]
