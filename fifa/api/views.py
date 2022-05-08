import re
from .serializers import *
from .models import *

from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count, Q

from rest_framework.parsers import MultiPartParser
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    create=extend_schema(
        tags=['Equipos'],
        summary="Creacion",
        description="Creacion de un nuevo equipo",
        request=EquipoSerializer,
        responses=EquipoJugadoresTecnicosSerializer),
    list=extend_schema(
        tags=['Equipos'],
        summary="Listado",
        description="Listado de los Equipos, con los jugadores y cuerpo tecnico registrados",
    ),
    update=extend_schema(
        exclude=True,
        tags=['Equipos'],
        summary="Actualizacion",
        description="Actualizacion de un equipo existente",
    ),
    partial_update=extend_schema(
        tags=['Equipos'],
        summary="Actualizacion Parcial",
        description="Actualizacion parcial de la informacion de un equipo existente"),
    destroy=extend_schema(
        tags=['Equipos'],
        summary="Eliminacion",
        description="Eliminacion de un equipo ingresando el identificador"),
    retrieve=extend_schema(
        tags=['Equipos'],
        summary="Informacion Base",
        description="Informacionde UN equipo ingresando el identificador"),
)
class EquipoViewSet(viewsets.ModelViewSet):
    serializer_class = EquipoJugadoresTecnicosSerializer
    queryset = Equipo.objects.all()
    parser_classes = [MultiPartParser]


class JugadorViewSet(viewsets.ViewSet):
    serializer_class = JugadorSerializer
    queryset = Jugador.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return JugadorEquipoSerializer
        return self.serializer_class
    
    @extend_schema(
        description="Crea un nuevo jugador",
        summary="Creacion",
        tags= ['Jugadores'],
        responses=JugadorEquipoSerializer
    )
    def create(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = JugadorEquipoSerializer(
            Jugador.objects.get(id=serializer.data["id"]))
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        description="Lista de jugadores registrados",
        summary="Listado",
        tags=['Jugadores'],
    )
    def list(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(Jugador.objects.all(), many=True)
        return Response(serializer.data)

    @extend_schema(
        
        description="Actualizacion de un jugador",
        summary="Actualizacion",
        tags=['Jugadores'],
        request=JugadorSerializer,
        responses=JugadorEquipoSerializer
    )
    def update(self, request, pk=None):
        item = get_object_or_404(Jugador.objects.all(), id=pk)
        serializer = self.get_serializer_class()
        serializer = serializer(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = JugadorEquipoSerializer(
            Jugador.objects.get(id=serializer.data["id"]))
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        description="Informacion de un Jugador ingresando el identificador",
        summary="Informacion",
        tags=['Jugadores'],
    )
    def retrieve(self, request, pk=None):
        item = get_object_or_404(Jugador.objects.all(), id=pk)
        serializer = self.get_serializer_class()
        serializer = serializer(item)
        return Response(serializer.data)

    @extend_schema(
        description="Eliminacion de un Jugador ingresando el identificador",
        summary="Eliminacion",
        tags=['Jugadores'],
    )
    def destroy(self, request,  pk=None):
        item = get_object_or_404(Jugador.objects.all(), id=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TecnicoViewSet(viewsets.ViewSet):
    serializer_class = TecnicoSerializer
    queryset = Tecnico.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TecnicoEquipoSerializer
        return self.serializer_class

    @extend_schema(
        description="Creacion de un miembro del cuerpo tecnico",
        summary="Creacion",
        tags=['Cuerpo Tecnico'],
        responses=TecnicoEquipoSerializer
    )
    def create(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = TecnicoEquipoSerializer(
            Tecnico.objects.get(pk=serializer.data["id"]))
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        description="Listado de miembros del cuerpo tecnico ",
        summary="Listado",
        tags=['Cuerpo Tecnico'],
    )
    def list(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(self.queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        description="Actualizacion de un miembro del cuerpo tecnico ",
        summary="Actualizacion",
        tags=['Cuerpo Tecnico'],
        responses=TecnicoEquipoSerializer
    )
    def update(self, request, pk=None):
        item = get_object_or_404(self.queryset, id=pk)
        serializer = self.get_serializer_class()
        serializer = serializer(
            item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = TecnicoEquipoSerializer(
            Tecnico.objects.get(pk=serializer.data["id"]))
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    @extend_schema(
        description="Informacion de un miembro del cuerpo tecnico ",
        summary="Informacion",
        tags=['Cuerpo Tecnico'],
        responses=TecnicoEquipoSerializer
    )
    def retrieve(self, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer_class()
        serializer = serializer(item)
        return Response(serializer.data)

    @extend_schema(
        description="Eliminacion de un miembro del cuerpo tecnico con su id",
        summary="Eliminacion",
        tags=['Cuerpo Tecnico'],
    )
    def destroy(self, pk=None):
        item = get_object_or_404(self.queryset, id=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    get=extend_schema(
    description="Reporte General de la informacion almacenada en la Base de datos",
    summary="Reporte de Datos",
    tags=['Reporte']
))
@api_view(['GET'])
def report(request):
    if request.method == 'GET':
        response = {
            'Equipos Registrados': Equipo.objects.count(),
            'Total Jugadores': Jugador.objects.count(),
            'Jugador mas joven': JugadorEquipoSerializer(Jugador.objects.order_by('-fecha_nacimiento').first()).data,
            'Jugador mas viejo': JugadorEquipoSerializer(Jugador.objects.order_by('fecha_nacimiento').first()).data,
            'Total Suplentes': Jugador.suplentes.all().count(),
            'Equipo con mas jugadores': EquipoSerializer(Equipo.objects.annotate(num_jugadores=Count('jugadores')).order_by('-num_jugadores').first()).data,
            'Promedio Edad': Jugador.objects.promedio_edad().all().aggregate(Avg('edad_prom'))['edad_prom__avg'],
            'Numero de Suplentes Promedio': Equipo.objects.annotate(num_suplentes=Count('jugadores', filter=Q(jugadores__titular=False))).aggregate(Avg('num_suplentes'))['num_suplentes__avg'],
            'Numero de Jugadores en promedio': Equipo.objects.annotate(num_jugadores=Count('jugadores')).aggregate(Avg('num_jugadores'))['num_jugadores__avg'],
            'Tecnico mas Viejo': TecnicoEquipoSerializer(Tecnico.objects.filter(rol='T').order_by('fecha_nacimiento').first()).data,
        }
        return Response(response)