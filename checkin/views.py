from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from .serializers import *
import datetime
from django.db import IntegrityError


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('rollNo')
    serializer_class = UserSerializer

def get_slot():
    now = datetime.datetime.now().time()
    print(now)
    breakfast_start = datetime.time(0, 0)
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
    def create(self, request):
        rollNo = request.data.get('rollNo')
        user = User.objects.filter(rollNo=rollNo).first()
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        slot = get_slot()
        if not slot:
            return Response({'error': 'Invalid time for check-in'}, status=status.HTTP_400_BAD_REQUEST)
        
        data = {'user': user.id, 'rollNo': user.rollNo, 'name': user.name, 'slot': slot}
        serializer = CheckInSerializer(data=data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'error': 'Already checked-in for this slot'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
