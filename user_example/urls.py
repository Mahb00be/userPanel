from django.urls import path
from . import views
from .views import doctor_list, doctor_name, doctor_city, send_comment, favorite_doctors
from .views import doctor_degree, doctor_expertise, edit_user, visit_request, edit_userpanel

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('doctorlist/', doctor_list),
    path('doctorcity/', doctor_city),
    path('doctorname/', doctor_name),
    path('doctordegree/', doctor_degree),
    path('doctorexpertise/', doctor_expertise),
    path('edit_user/<int:pk>', edit_user),
    path('send_comment/', send_comment),
    path('visit_request/', visit_request),
    path('favorite_doctors/<int:pk>', favorite_doctors),
    path('edit_userpanel/', edit_userpanel),

]
