from rest_framework import serializers
from .models import *
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample



@extend_schema_serializer(
    
    examples=[
        OpenApiExample(
            'Ejemplo',
            summary='Un Equipo',
            description='Respuesta informacion de un Equipo',
            value={
                        "id": 1,
                        "nombre": "Real Madrid",
                        "bandera": "/bandera1.png",
                        "escudo": "/escudo1.png"
            },
            request_only=True, 
            response_only=False,
        ),
    ]
)
class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = '__all__'


@extend_schema_serializer(
      
    examples=[
        OpenApiExample(
            'Ejemplo',
            summary='Jugador',
            description='Respuesta serializacíon de un jugador con info del equipo perteneciente.',
            value={
                    "id": 1,
                    "equipo": {
                        "id": 1,
                        "nombre": "Real Madrid",
                        "bandera": "/bandera1.png",
                        "escudo": "/escudo1.png"
                    },
                    "edad": 20,
                    "nombre": "Daniel",
                    "apellido": "Lopez",
                    "fecha_nacimiento": "2000-08-10",
                    "posicion": "Delantero",
                    "numero": 10,
                    "titular": "true"
            },
            request_only=False, 
            response_only=True,
        ),
    ]
)
class JugadorEquipoSerializer(serializers.ModelSerializer):
    equipo = EquipoSerializer()
    edad = serializers.ReadOnlyField()
    class Meta:
        model = Jugador
        fields = '__all__'
        depht = 1



@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Ejemplo',
            summary='Cuerpo Tecnico',
            description='Ingreso de un miembro del cuerpo Tecnico con la info del equipo perteneciente',
            value={
                "id": 1,
                "equipo": {
                    "id": 1,
                    "nombre": "Real Madrid",
                    "bandera": "/bandera1.png",
                    "escudo": "/escudo1.png"
                },
                "edad": 30,
                "nombre": "Pepito",
                "apellido": "Perez",
                "fecha_nacimiento": "2000-01-01",
                "nacionalidad": "Colombiano",
                "rol": "Tecnico",
            },
            request_only=False, 
            response_only=True,
        ),
    ]
)
class TecnicoEquipoSerializer(serializers.ModelSerializer):
    equipo = EquipoSerializer()
    edad = serializers.ReadOnlyField()
    class Meta:
        model = Tecnico
        fields = '__all__'
        depht = 1


@extend_schema_serializer(
    
    examples=[
        OpenApiExample(
            'Ejemplo',
            summary='Jugador',
            description='Ingreso de un jugador con el campo de equipo perteneciente',
            value={
                "id": 1,
                "equipo": 1,
                "nombre": "Daniel",
                "apellido": "Lopez",
                "fecha_nacimiento": "2000-08-10",
                "posicion": "Delantero",
                "numero": 10,
                "titular": "true"
            },
            request_only=True, 
            response_only=False,
        ),
    ]
)
class JugadorSerializer(serializers.ModelSerializer):
    equipo = serializers.PrimaryKeyRelatedField(many=False, queryset=Equipo.objects.all())
    
    class Meta:
        model = Jugador
        fields = '__all__'
        depht = 1


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Ejemplo',
            summary='Cuerpo Tecnico',
            description='Respuesta serializacíon de un miembro del cuerpo Tecnico con el equipo perteneciente',
            value={
                "id": 1,
                "equipo": 1,
                "nombre": "Pepito",
                "apellido": "Perez",
                "fecha_nacimiento": "2000-01-01",
                "nacionalidad": "Colombiano",
                "rol": "Tecnico",
            },
            request_only=False, 
            response_only=True,
        ),
    ]
)
class TecnicoSerializer(serializers.ModelSerializer):
    equipo = serializers.PrimaryKeyRelatedField(many=False, queryset=Equipo.objects.all())
    class Meta:
        model = Tecnico
        fields = '__all__'
        depht = 1


@extend_schema_serializer(
    
    examples=[
        OpenApiExample(
            'Ejemplo',
            summary='Equipo',
            description='Respuesta info de un Equipo con la info serializada de los jugadores y el cuerpo tecnico',
            value={
                    "id": 1,
                    "nombre": "Real Madrid",
                    "bandera": "bandera1.png",
                    "escudo": "escudo1.png",
                    "jugadores": [
                        {
                            "id": 1,
                            "equipo": 1,
                            "edad": 20,
                            "nombre": "Daniel",
                            "apellido": "Lopez",
                            "fecha_nacimiento": "2000-08-10",
                            "posicion": "Delantero",
                            "numero": 10,
                            "titular": "true"
                        }
                    ],
                    "tecnicos": [
                            {
                                "id": 1,
                                "equipo": 1,
                                "edad": 30,
                                "nombre": "Pepito",
                                "apellido": "Perez",
                                "fecha_nacimiento": "2000-01-01",
                                "nacionalidad": "Colombiano",
                                "rol": "Tecnico",
                            }
                        ],
            },
            request_only=True, 
            response_only=False,
        ),
    ]
)
class EquipoJugadoresTecnicosSerializer(serializers.ModelSerializer):
    jugadores = JugadorSerializer(many=True, read_only=True)
    tecnicos= TecnicoSerializer(many=True, read_only=True)
    class Meta:
        model = Equipo
        fields = '__all__'
