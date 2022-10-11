from dataclasses import dataclass
from functools import partial
from gettext import find
from itertools import count
import json
from os import stat
from TimeManage.exceptions import NoneAuthorized
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from .serializers import ReadySerializer, RelationSerializer, StylesSerializer, TotalSerializer, UserSerializer, LabsSerializer
from rest_framework.permissions import *
from rest_framework.views import APIView
from .models import *
from django.core.paginator import Paginator
import math
from rest_framework import status

class UserView(APIView):
    def get(self, request):
        try:
            if not request.user.pk:
                raise Exception()
            w = User.objects.filter(pk = request.user.pk)
            return Response(UserSerializer(w[0]).data)
        except:
            return Response(status=404, data={'error': 'Token not found'})

class StylesViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = CardStyles.objects.all()
    serializer_class = StylesSerializer
    permission_classes = (IsAuthenticated,)

class LabsViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):

    queryset = Laboratories.objects.all()
    serializer_class = LabsSerializer

class RelationView(APIView):
    def get(self, request):
        try:
            if not request.user.pk:
                raise NoneAuthorized()
            page = request.GET.get("page", '')
            relations = Relations.objects.filter(userID = request.user.pk)
            paginator = Paginator(relations, 10)
            return Response(RelationSerializer(paginator.page(page), many=True).data)
        except NoneAuthorized as e:
            return Response(status=403, data={'error': 'Invalid token'})
        except:
            return Response(status=500, data={'error': 'Something went wrong.'})

    def post(self, request):
        labSerizalizer = LabsSerializer(data={"name": request.data.get('labName'), "count":request.data.get('count'), "deadline": request.data.get('deadline')})
        try:
            if not request.user.pk:
                raise NoneAuthorized()
            getStyle = CardStyles.objects.get(pk=request.data.get('style'))
            if not getStyle:
                raise Exception()
        except NoneAuthorized as e:
            return Response(status=403, data={'error': 'Invalid token'})
        except:
            return Response(status=404, data={'error': 'Incorrect style'})
        if labSerizalizer.is_valid(raise_exception=True):
            laba_saved = labSerizalizer.save()
            Relations.objects.create(styleID=CardStyles.objects.get(pk=request.data.get('style')), userID=User.objects.get(pk=request.user.pk), labID=Laboratories.objects.get(pk=laba_saved.pk))
            return Response({"success": "Relation '{}' created successfully".format(laba_saved.name)}, status=200)
        else:
            return Response(status=500, data={'error': 'Something went wrong.'})

    def delete(self, request):
        try:
            labID = request.data.get('id')
            findLab = Laboratories.objects.get(pk = labID)
            findLab.delete()
            return Response(LabsSerializer(findLab).data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None, format=None):
        if not id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            style = int(request.GET.get('style',''))
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        relation = Relations.objects.get(labID = id)
        laboratory = Laboratories.objects.get(pk=id)
        labSerializer = LabsSerializer(laboratory, data=request.data)
        if labSerializer.is_valid(raise_exception=True):
            relation.styleID = CardStyles.objects.get(pk=style)
            relation.save()
            labSerializer.save()
            return Response(labSerializer.data,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
class RelationSearch(APIView):
    def get(self,request):
        searchtext = request.GET.get("text", '')
        allLabs = Laboratories.objects.filter(name__contains=searchtext)
        allRelations = Relations.objects.filter(userID = request.user.pk)
        data = []
        for relation in allRelations:
            for lab in allLabs:
                if(relation.labID.id == lab.id):
                    data.append(relation)
        return Response(RelationSerializer(data, many=True).data)

class TotalView(APIView):
    def get(self,request):
        try:
            if not request.user:
                raise NoneAuthorized()
        except NoneAuthorized as e:
            return Response(status=403, data={'error': 'Invalid token'})
        except:
            return Response(status=status.HTTP_401_U)
        relations = Relations.objects.filter(userID = request.user.pk)
        data = {'count': math.ceil(relations.count()/10)}
        total = TotalSerializer(data).data
        return Response(total,status=200)

class ReadyTasksView(APIView):
    def get(self,request,id = None):
        try:
            if not id:
                raise Exception()
            if not request.user:
                raise NoneAuthorized()
            ready = ReadyTasks.objects.filter(user_id = request.user.pk).filter(lab_id = id)
            return Response(ReadySerializer(ready, many=True).data)
        except NoneAuthorized as e:
            return Response(status=403, data={'error': 'Invalid token'})
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            if not request.user:
                raise NoneAuthorized()
            data = request.data.copy()
            data.update({"user": request.user.pk})
            serializer = ReadySerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                labid = serializer.validated_data.get("lab").pk
                serializer.save()
                laboratory = Laboratories.objects.get(pk=labid)
                updateSerializer = LabsSerializer(laboratory, data={"ready": ReadyTasks.objects.filter(lab_id=labid).count()}, partial=True)
                if(updateSerializer.is_valid(raise_exception=True)):
                    updateSerializer.save()
                    return Response(serializer.data)
            return Response(status=status.HTTP_200_OK)
        except NoneAuthorized as e:
            return Response(status=403, data={'error': 'Invalid token'})
        except:
            return Response(status=500, data={'error': 'Something went wrong.'})
        
    def delete(self,request):
        ready_task = request.data.get('ready_task')
        lab = request.data.get('lab')
        try:
            if not ready_task or not lab:
                raise Exception()
            task = ReadyTasks.objects.filter(ready_task=int(request.data.get('ready_task'))).filter(lab_id=request.data.get('lab'))[0]
            task.delete()
            laboratory = Laboratories.objects.get(pk=lab)
            updateSerializer = LabsSerializer(laboratory, data={"ready": ReadyTasks.objects.filter(lab_id=lab).count()}, partial=True)
            if(updateSerializer.is_valid(raise_exception=True)):
                updateSerializer.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        lab = request.data.get('lab')
        try:
            if not lab:
                raise Exception()
            tasks = ReadyTasks.objects.filter(lab_id=lab)
            for item in tasks:
                item.delete()
            laboratory = Laboratories.objects.get(pk=lab)
            updateSerializer = LabsSerializer(laboratory, data={"ready": ReadyTasks.objects.filter(lab_id=lab).count()}, partial=True)
            if(updateSerializer.is_valid(raise_exception=True)):
                updateSerializer.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)