
<div id="top"></div>

<div align="center">
  <h1 align="center">Fifa Api</h1>
    <br />
</div>
<br />


## Enunciado

La FIFA me ha contactado para que le ayudes a consolidar la información de todos los equipos que van a ir al próximo mundial, así que te dicen que debes crear una API con un CRUD para cada una de la siguiente información:
* Equipo:
  * Nombre del Equipo
  * Imagen de Bandera
  * Escudo del Equipo
* Jugadores del equipo, con los siguientes datos de cada jugador:
  * Foto del jugador
  * Nombre
  * Apellido
  * Fecha de nacimiento
  * Posición en la que juega
  * Número de camiseta
  * ¿Es titular?
* Cuerpo técnico
  * Nombre
  * Apellido
  * Fecha de nacimiento
  * Nacionalidad
  * Rol (técnico | asistente | médico | preparador)

### Construido con 

La API fue desarrollada con:.

* Python
* Django
* Django Rest Framework
* MySQL

## Guia de Uso

#### Instalanción mediante entorno virtual

Es necesario contar con Python 3.7 o superior e instalar los requerimientos del archivo requirements.txt.

* Creacion del entorno virtual:
```
$ python3 -m pip install virtualenv
$ python3 -m virtualenv venv
```
* Activamos el entorno virtual:
    ```
      $ .\venv\Scripts\activate
    ```
* Instalar requerimientos
  ```
    $ pip install -r requirements.txt
  ```

Es requisito contar con MySQL (con laravel o wamp). 
La configuracion de la base de datos esta en el archivo settings.py.

* Inicio de la api:
```
$ python manage.py runserver
```
