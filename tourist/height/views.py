from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import *
from .models import *


class UserViewset(viewsets.ModelViewSet):
   queryset = AddUser.objects.all()
   serializer_class = AddUserSerializer


class CoordsViewset(viewsets.ModelViewSet):
   queryset = Coords.objects.all()
   serializer_class = CoordsSerializer


class LevelViewset(viewsets.ModelViewSet):
   queryset = Level.objects.all()
   serializer_class = LevelSerializer


class MountViewest(viewsets.ModelViewSet):
   queryset = Mount.objects.all()
   serializer_class = MountSerializer
   filterset_fields = ('user__email',)

   def create(self, request, *args, **kwargs):

      serializer = MountSerializer(data=request.data)

      if serializer.is_valid():
         serializer.save()
         response = {'status': 200,
                     'message': '',
                     'id': serializer.data.get('id')}
      elif status.HTTP_500_INTERNAL_SERVER_ERROR:
         response = {'status': 500,
                     'message': 'Ошибка подключения к базе данных',
                     'id': serializer.data.get('id')}
      elif status.HTTP_400_BAD_REQUEST:
         response = {'status': 400,
                     'message': 'Неверный запрос',
                     'id': serializer.data.get('id')}
      return Response(response)


   def partial_update(self, request, *args, **kwargs):

      instance = self.get_object()
      serializer = MountSerializer(instance, data=request.data, partial=True)

      if request.data['status'] == 'new':
         if serializer.is_valid():
            serializer.save()
            response = {'state': 1,
                        'message': 'Успешное изменение данных.'}
            return Response(response, status=status.HTTP_200_OK)
         else:
            response = {'state': 0,
                        'message': 'Данные о пользователе менять нельзя!'}
            return Response(response, status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)
      else:
         response = {'state': 0,
                     'message': 'Ошибка. Данные проходят модерацию.'}
         return Response(response, status=status.HTTP_204_NO_CONTENT)


   def get_queryset(self):
      queryset = Mount.objects.all()
      user = self.request.query_params.get('user__email', None)
      if user is not None:
         queryset = queryset.filter(user__mail=user)
      return queryset


class PhotoViewest(viewsets.ModelViewSet):
   queryset = Photo.objects.all()
   serializer_class = PhotoSerializer