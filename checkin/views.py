from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from .serializers import *
import datetime
from django.db import IntegrityError
# from django.db.models import Q
from datetime import timedelta
import pandas as pd
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from django.contrib.auth.decorators import permission_required
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)

        user_permissions = user.user_permissions.all()
        permissions_list = [p.codename for p in user_permissions]
        print('-------------------------', permissions_list)

        user_type = None
        if 'can_manage_all' in permissions_list:
            user_type = 'admin'
        elif 'can_view_stats' in permissions_list:
            user_type = 'HCM'
        elif 'can_check_in' in permissions_list:
            user_type = 'Mess Worker'

        return Response({'token': token.key, 'success': 'Login successful', 'user_type': user_type}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout_view(request):
    request.auth.delete()
    return Response(status=status.HTTP_200_OK)

class CanCheckInPermission(BasePermission):
    message = "You don't have permission to check in."

    def has_permission(self, request, view):
        return request.user.has_perm('checkin.can_check_in')

class CanViewStatsPermission(BasePermission):
    message = "You don't have permission to view statistics."

    def has_permission(self, request, view):
        # return request.user.has_perm('checkin.can_view_stats')
        return True


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all().order_by('rollNo')
    serializer_class = UserSerializer
    
    # @permission_required('checkin.can_view_stats')
    def retrieve(self, request, pk=None):
        try:
            print("or here")
            if not request.user.has_perm('checkin.can_view_stats'):
                return Response({'error': 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)
            user = User.objects.filter(rollNo=pk).first()
            if not user:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

def get_slot():
    now = datetime.datetime.now().time()
    print(now)
    breakfast_start = datetime.time(7, 0)
    breakfast_end = datetime.time(10, 0)
    lunch_start = datetime.time(12, 0)
    lunch_end = datetime.time(14, 30)
    snacks_start = datetime.time(16, 0)
    snacks_end = datetime.time(18, 30)
    dinner_start = datetime.time(19, 0)
    dinner_end = datetime.time(21, 30)

    if breakfast_start <= now <= breakfast_end:
        return 'breakfast'
    elif lunch_start <= now <= lunch_end:
        return 'lunch'
    elif snacks_start <= now <= snacks_end:
        return 'snacks'
    elif dinner_start <= now <= dinner_end:
        return 'dinner'
    else:
        return None
    
class CheckInViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        rollNo = request.data.get('rollNo')
        user = User.objects.filter(rollNo=rollNo).first()

        if not CanCheckInPermission().has_permission(request, self):
            return Response({'error': CanCheckInPermission.message}, status=status.HTTP_403_FORBIDDEN)
        
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        slot = get_slot()
        if not slot:
            return Response({'error': 'Invalid time for check-in'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        today = datetime.datetime.now().date()
        existing_checkin = CheckIn.objects.filter(user=user, date=today, slot=slot).first()
        if existing_checkin:
            return Response({'error': 'Already checked-in for this slot'}, status=status.HTTP_403_FORBIDDEN)

        data = {'user': user.id, 'rollNo': user.rollNo, 'name': user.name, 'slot': slot}
        serializer = CheckInSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        queryset = CheckIn.objects.all()
        
        date = request.query_params.get('date', None)
        last_30_days = request.query_params.get('last_30_days', None)
        slot = request.query_params.get('slot', None)
        rollNo = request.query_params.get('rollNo', None)
        food_type = request.query_params.get('food_type', None)
        last_7_days = request.query_params.get('last_7_days', None)

        if not CanViewStatsPermission().has_permission(request, self):
            return Response({'error': CanViewStatsPermission.message}, status=status.HTTP_403_FORBIDDEN)
        

        if date:
            queryset = queryset.filter(date=date)
        elif not date:
            queryset = queryset.filter(date=datetime.datetime.now().date())
        if last_30_days:
            end_date = datetime.datetime.now().date()
            start_date = end_date - timedelta(days=30)
            queryset = queryset.filter(date__range=(start_date, end_date))
        if last_7_days:
            end_date = datetime.datetime.now().date()
            start_date = end_date - timedelta(days=7)
            queryset = queryset.filter(date__range=(start_date, end_date))

        if slot:
            queryset = queryset.filter(slot=slot)
        
        if rollNo:
            queryset = queryset.filter(rollNo=rollNo)
        
        if food_type:
            queryset = queryset.filter(food_type=food_type)

        paginator = Paginator(queryset, 50)
        page = request.query_params.get('page', 1)

        try:
            checkins = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            checkins = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            checkins = paginator.page(paginator.num_pages)

        serializer = CheckInSerializer(checkins, many=True)
        return Response({
            'count': paginator.count,
            'next': None if not checkins.has_next() else checkins.next_page_number(),
            'previous': None if not checkins.has_previous() else checkins.previous_page_number(),
            'data': serializer.data
        })
    
class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_class = (FileUploadParser,)

    @permission_required('checkin.can_manage_all')
    def post(self, request):
        file_serializer = FileSerializer(data=request.data)

        if file_serializer.is_valid():
            file_obj = file_serializer.validated_data['file']
            if file_obj.name.endswith('.csv'):
                data = pd.read_csv(file_obj)
            elif file_obj.name.endswith('.xlsx'):
                data = pd.read_excel(file_obj)

            for index, row in data.iterrows():
                user = User(
                    rollNo=row['rollNo'],
                    type=row['type'],
                    batch=row['batch'],
                    name=row['name'],
                    hall=row['hall'],
                    # profile pic code
                )
                user.save()

            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)