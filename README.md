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

## Requisitos
En el caso de no utilizar el script `set-venv.sh`, será necesario instalar manualmente la librería de `flask-restful` para poder ejecutar el programa. Para ello se puede hacer uso del `requirements.txt` para instalarla.

```
$ pip install -r requirements.txt
```

## Lanzamiento de pruebas automáticas


Por si te da la neura de nuevo, por aqui dejo esto de los jwt en python xd
https://realpython.com/token-based-authentication-with-flask/#database-setup
