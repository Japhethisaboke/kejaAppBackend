import requests
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from random import randint, shuffle

from .serializers import *

# Create your views here.

""" Views for users:-
 1. Getting all users. 
 2. Getting user details of a specific user
 """


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def user_list(request, *args, **kwargs):
    users = User.objects.all()
    serializer = UserCreateSerializer(users, context={"request": request}, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def user_detail_email(request, email, *args, **kwargs):
    try:
        user = User.objects.get(email__contains=email)
        serializer = UserCreateSerializer(user, context={"request": request})
        return JsonResponse(serializer.data)
    except User.DoesNotExist:
        return Response(data={}, status=404)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def user_detail_id(request, id, *args, **kwargs):
    try:
        user = User.objects.get(pk=id)
        serializer = UserCreateSerializer(user, context={"request": request})
        return JsonResponse(serializer.data)
    except User.DoesNotExist:
        return Response(data={}, status=404)


# Reset password, send activation email and resend activation email.
@api_view(['GET'])
def activation(request, uid, token, *args, **kwargs):
    protocol = 'https://' if request.is_secure() else 'http://'
    web_url = protocol + request.get_host()
    post_url = web_url + '/houses/users/activation/'
    post_data = {'uid': uid, 'token': token}
    response = requests.post(post_url, data=post_data)
    if response.status_code == 204:
        return render(request, 'houses/success_activation.html')
    else:
        return render(request, 'houses/unsuccessful_activation.html')


@api_view(['GET', 'POST'])
def reset(request, uid, token, *args, **kwargs):
    if request.POST:
        new_password = request.POST.get('new_password')
        re_new_password = request.POST.get('re_new_password')
        post_data = {'uid': uid, 'token': token, 'new_password': new_password, 're_new_password': re_new_password}

        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + '/houses/users/reset_password_confirm/'

        response = requests.post(post_url, data=post_data)
        if response.status_code == 204:
            return render(request, 'houses/success_reset.html')
        else:
            return render(request, 'houses/unsuccessful_reset.html')
    else:
        return render(request, 'houses/reset_password.html')


""" Views for houses:-
 1. Getting all houses. 
 2. Getting houses around a certain point
 3. Creating a house
 n/b a function for populating house_images and binding them to the res data
 """


@api_view(['GET'])
def get_houses(request):
    try:
        house = House.objects.all()
        house_serializer = HouseSerializer(house, many=True).data
        updates_houses = get_house_images(house_serializer)
        return Response(updates_houses)
    except House.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_shuffled_houses(request):
    try:
        house = list(House.objects.all()[:30])
        shuffle(house)
        house_serializer = HouseSerializer(house, many=True).data
        updates_houses = get_house_images(house_serializer)
        return Response(updates_houses)
    except House.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_houses_random(request):
    try:
        house = House.objects.all()
        length = house.count()
        if length < 12:
            start = 0
            end = 6
        else:
            end = randint(6, length)
            start = end - 6
        house = House.objects.all()[start:end]
        house_serializer = HouseSerializer(house, many=True).data
        updates_houses = get_house_images(house_serializer)
        return Response(updates_houses)
    except House.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_houses_category_id(request, category_id):
    try:
        house = House.objects.filter(category=category_id)
        house_serializer = HouseSerializer(house, many=True).data
        updates_houses = get_house_images(house_serializer)
        return Response(updates_houses)
    except House.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_houses_owner_id(request, owner_id):
    try:
        house = House.objects.filter(owner=owner_id)
        house_serializer = HouseSerializer(house, many=True).data
        updates_houses = get_house_images(house_serializer)
        return Response(updates_houses)
    except House.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_houses_around_specific_point(request):
    try:
        latitude = float(request.GET.get('latitude', ''))
        longitude = float(request.GET.get('longitude', ''))
    except ValueError:
        return Response({'Error': 'Please pass the latitude and longitude as url parameters'},
                        status=status.HTTP_404_NOT_FOUND)

    user_location = Point(longitude, latitude, srid=4326)
    try:
        house = House.objects.annotate(distance=Distance('location', user_location)).order_by('distance')[0:50]
        house_serializer = HouseSerializer(house, many=True).data
        updates_houses = get_house_images(house_serializer)
        return Response(updates_houses)
    except House.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', 'PATCH'])
def create_house(request):
    data = request.data
    serializer = HouseSerializer(data=data)
    try:
        if serializer.is_valid('raise_exception'):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except serializers.ValidationError as error:
        print(error)
        return Response(status=status.HTTP_400_BAD_REQUEST)


def get_house_images(houses_obj):
    for house in houses_obj['features']:
        house_images = HouseImages.objects.filter(house=house['id']).only('id', 'image')
        house_images_serializer = HouseImagesSerializer(house_images, many=True)
        image_link_array = []
        for image in house_images_serializer.data:
            image_link_array.append(image['image'])
        house['properties'].update(house_images=image_link_array)
    return houses_obj


"""create house images. The if is for when we put a get request"""


@api_view(['POST'])
def house_image(request):
    if request.method == 'POST':
        data = request.data
        if 'houseId' in data:
            new_house_id = data['houseId']
            del data['houseId']
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            for image in data.values():
                house_image_data = {'house': new_house_id, 'image': image}
                house_image_serializer = HouseImagesSerializer(data=house_image_data)
                if house_image_serializer.is_valid('raise_exception'):
                    house_image_serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


"""get house categories. """


@api_view(['GET'])
def get_categories(request):
    try:
        category = Category.objects.all()
        category_serializer = CategorySerializer(category, many=True)
        return Response(category_serializer.data)
    except House.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
