# Práctica 3 - Seguridad en Redes

## Integrantes
Alberto Vázquez Martínez - Alberto.Vazquez1@alu.uclm.es

Paulino de la Fuente Lizcano - Paulino.Lafuente@alu.uclm.es

## Certificados

Para utilizar el protocolo https, es necesario copiar el archivo **cert.perm** a la ruta *usr/local/share/ca-certificates*, una vez ahí, se debe modificar el nombre a **cert.crt** y actualizar la lista de certificados para que la herramienta curl reconozca el certificado 

```
$ sudo update-ca-certificates cert.crt
```

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

Para el lanzamiento de las pruebas automáticas es necesario tener instalado dos herramientas: **curl** y **jq**. Si no las tienes installadas puede utilizar el siguiente comando:

```
$ sudo apt-get install curl jq
```

Para lanzar cada uno de los scripts de prueba es necesario primero lanzar el servidor. Para ello, simplemente hay que ejecutar el script de python `main.py`.

```
$ python3 ./main.py
```

### Version
```bash
$ ./test_version.sh
```
### Login y signup
```bash
$ ./test_register_login.sh <user> <password>

# Ejemplo
$ ./test_register_login.sh alberto password
```

### Archivos JSON
```bash
$ ./test_user_actions.sh <user> <password> <doc_id>

# Ejemplo
$ ./test_user_actions.sh alberto password documento
```

### Listar todos los documentos de un usuario
```bash
$ ./test_all_docs.sh <user> <password>

# Ejemplo
$ ./test_all_docs.sh paulino paulino
```
<!-- Por si te da la neura de nuevo, por aqui dejo esto de los jwt en python xd
https://realpython.com/token-based-authentication-with-flask/#database-setup -->
