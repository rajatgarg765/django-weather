
from rest_framework.response import Response
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer
from rest_framework import status
from django.contrib.auth import authenticate
import urllib
import json
from django.http import JsonResponse
from account.serializers import UserLoginSerializer
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from threading import Timer

# Create your views here.
#generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token= get_tokens_for_user(user)
            return Response({'token':token,'msg':"Registration Success"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if(serializer.is_valid(raise_exception=True)):
            username=serializer.data.get('username')
            password=serializer.data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                token= get_tokens_for_user(user)
                return Response({'token':token,'msg':"Login Success"},status=status.HTTP_200_OK)
            else:
                return Response({'errros':{'non_field_errors':['Username or Password is not valid']}},status=status.HTTP_404_NOT_FOUND)

weather_list=[]
def fetchData():
    city_id=[1788081,1809532,2033536,2034657,1784055,1785964,2034497,1853909,1848354,2111749,1859740,1859171,1863431,1863967,1859924,1894616,1855431,2113015,1864154,1856215,2111220,2113077,1856717,1864624,1857910,2112923,1858729,1856697,1848254,1849876]
    count=1
    global weather_list
    weather_list = []
    for i in range(30):
        source = urllib.request.urlopen('https://api.openweathermap.org/data/2.5/weather?id='+str(city_id[i])+'&appid=818433e77106355df28167ab88f71959').read()
        list_of_data = json.loads(source)
        list_of_data['id']=count
        weather_list.append(list_of_data)
    print("Data loaded")
    Timer(1800,fetchData).start()
fetchData()

class CheckWeather(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        try:
            pageNum = request.GET["pageNum"]
            if pageNum=="":
                page=1
            else:
                page=int(pageNum)
            if page==1:
                start=0
                end=10
            elif page==2:
                start=10
                end=20
            else:
                start=20
                end=30
            return JsonResponse({'page_obj': weather_list[start:end]},status=status.HTTP_200_OK)
        except:
            start=0
            end=10
            return JsonResponse({'page_obj': weather_list[start:end]},status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes=[UserRenderer]
    def post(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})
        refresh_token = self.request.data.get('refresh_token')
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"status": "OK, goodbye"})


