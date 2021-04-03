from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from .forms import UserPanelForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Doctor, Comment
from .models import UserPanel, User
from .serializers import DoctorSerializer, UserPanelSerializer, UserSerializer, CommentSerializer, VisitSerializer
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from .permissions import IsOwner


# Create your views here.

def index(request):
    return render(request, 'user_example/index.html')


@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@permission_classes((AllowAny,))
def register(request):
    if request.method == 'POST':

        form = UserCreationForm(request.POST)
        userPanelForm = UserPanelForm(request.POST)

        if form.is_valid() and userPanelForm.is_valid():
            user = form.save()
            userpanel = userPanelForm.save(commit=False)
            userpanel.user = user
            userpanel.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')

    else:
        form = UserCreationForm()
        userPanelForm = UserPanelForm()

    context = {'form': form, 'userPanelForm': userPanelForm}
    return render(request, 'registration/register.html', context)


@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def doctor_list(request):
    if request.method == 'GET':
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((AllowAny,))
def doctor_city(request):
    doctors = Doctor.objects.filter(city=request.query_params['city'])
    if doctors:
        ser = DoctorSerializer(doctors, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((AllowAny,))
def doctor_name(request):
    doctors = Doctor.objects.filter(lastname=request.query_params['lastname'])
    if doctors:
        ser = DoctorSerializer(doctors, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((AllowAny,))
def doctor_degree(request):
    doctors = Doctor.objects.filter(educationDegree=request.query_params['educationDegree'])
    if doctors:
        ser = DoctorSerializer(doctors, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((AllowAny,))
def doctor_expertise(request):
    doctors = Doctor.objects.filter(medicalExpertise=request.query_params['medicalExpertise'])
    if doctors:
        ser = DoctorSerializer(doctors, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT'])
@permission_classes((IsAuthenticated,))
def edit_user(request, pk):
    try:
        user = UserPanel.objects.get(pk=pk)

    except:
        return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':

        ser = UserPanelSerializer(user)

        return Response(ser.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        ser = UserPanelSerializer(user, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def send_comment(request):
    if request.method == 'POST':
        data = {
            'user': request.data['user'],
            'doctor': request.data['doctor'],
            'text': request.data['text'],
        }

    ser1 = CommentSerializer(data=data)

    if ser1.is_valid():
        ser1.save()
        return Response(ser1.data, status=status.HTTP_200_OK)
    else:
        return Response(ser1.errors, status=status.HTTP_400_BAD_REQUEST)

# comments = Comment.objects.filter(user=request.query_params['user'])
#
# if request.method == 'GET':
#     ser = CommentSerializer(comments, many=True)
#     return Response(ser.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def visit_request(request):
    if request.method == 'POST':

        data = {
            'user': request.data['user'],
            'doctor': request.data['doctor'],
            'visitTime': request.data['visitTime'],
            'visitDate': request.data['visitDate'],
        }

    ser1 = VisitSerializer(data= data)

    if ser1.is_valid():
        ser1.save()
        return Response(ser1.data, status=status.HTTP_200_OK)
    else:
        return Response(ser1.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def favorite_doctors(request, pk):
    try:
        user = UserPanel.objects.get(pk=pk)
    except:
        return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        ser = UserPanelSerializer(user)
        # user.user.username
        return Response(ser.data.get('favoriteDoctors'), status=status.HTTP_200_OK)
    elif request.method == 'PUT':

        ser = UserPanelSerializer(user)

        data = {
            'user': ser.data.get('user'),
            'favoriteDoctors': request.data['favoriteDoctors'],
            'age': ser.data.get('age'),

        }

        ser1 = UserPanelSerializer(user, data=data)

        if ser1.is_valid():
            ser1.save()
            return Response(ser1.data, status=status.HTTP_200_OK)
        else:
            return Response(ser1.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes((IsAuthenticated,IsOwner,))
def edit_userpanel(request):
    try:
        user = UserPanel.objects.get(user=request.user.id)

    except:
        return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':

        ser = UserPanelSerializer(user)
        return Response(ser.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        ser = UserPanelSerializer(user, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)




