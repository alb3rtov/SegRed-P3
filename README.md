# Práctica 3 - Seguridad en Redes

## Integrantes
Alberto Vázquez Martínez - Alberto.Vazquez1@alu.uclm.es

Paulino de la Fuente Lizcano - Paulino.Lafuente@alu.uclm.es

## Configurar virtual enviroment
Para configurar automaticamente un virtual enviroment donde instalar las librerías necesarias, simplemente ejecuta el script `set-venv.sh` de la siguiente manera:

```
$ source set-venv.sh
```
De esta manera se configurará el virtual enviroment y se instalarán las librerías necesarias automáticamente.

Para desactivar el virtual enviroment, ejecuta el siguiente comando:

```
$ deactivate
```

## Modificar archivo para resolución DNS

Según el enunciado, debemos de acceder a la dirección `mylocal.server:5000` la cual se traduce en `127.0.0.1:5000`, por ello es necesario modificar el archivo **/etc/hosts** añadiendo una linea con la siguente información

```
127.0.0.1   mylocal.server
```

## Requisitos
En el caso de no utilizar el script `set-venv.sh`, será necesario instalar manualmente la librería de `flask-restful` para poder ejecutar el programa. Para ello se puede hacer uso del `requirements.txt` para instalarla.

```
$ pip install -r requirements.txt
```

## Lanzamiento de pruebas automáticas


Por si te da la neura de nuevo, por aqui dejo esto de los jwt en python xd
https://realpython.com/token-based-authentication-with-flask/#database-setup
