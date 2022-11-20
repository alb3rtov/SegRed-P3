# Práctica 3 - Seguridad en Redes

https://github.com/alb3rtov/SegRed-P3

## 1-Integrantes

Alberto Vázquez Martínez - Alberto.Vazquez1@alu.uclm.es

Paulino de la Fuente Lizcano - Paulino.Lafuente@alu.uclm.es

## 2-Explicación

Este proyecto simula un servicio de almacenamiento online donde se pueden crear usuarios, donde usuario tiene su espacio para poder subir archivos en formato **.json** ,
se dispone de un archivo llamado **.shadow** simulando el comportamiento de un entorno linux, donde se almacena el nombre de usuario, seguido de un codigo utilizado para generar el hash de la contraseña y por ultijmo se almacena el hash generado.

```
usuario:salt:hash
```

A su vez, se utilizan tokens para autorizar ciertas acciones de los usuarios, dichas acciones son:
1. **GET** sobre un archivo
2. **POST** de un archivo
3. **PUT** de un archivo existente
4. **DELETE** un archivo

Los tokens tienen un tiempo de uso, por defecto están configurados para que duren 5 minutos, en el caso de que se desee modificar el tiempo de vida del token, tan solo hay que modificar la varibale global **MINUTES**

Para la gestión de los tokens, hemos decidio usar 2 diccionarios llamados *TOKENS_DICT* y *EXP_TOKEN*, en el primero se asocia un token a un usuario y en el otro se asocia una fecha limite para poder ser usado. En el momento en que caduca, ambos diccionarios se sincronizan para que el token expirado se elimine y se genere otro si el usuario registrado introduce bien su id de usuario y su contraseña.

Para comunicarse con el servidor, es necesario utilizar el protocolo HTTPS, ya que si se usa el protocolo HTTP es denegado.


## 3-Generación de token de autenticación

Para la generación del token de autenticación de usuarios hemos optado por utilizar `UUIDs` (versión 4), ya que son identificadores únicos universales y así nos aseguramos de que el token no se repita para otro usuario. 

Cuando generamos un token, almacenamos la hora de creación del token para así poder comprobar si ha caducado o no.


## 4-Aspectos a mejorar

Es posible que si el programa es usado por muchos usuarios, sea necesario el limitar el espacio que estos pueden usar, si no, un usuario podria subir archivos muy pesados provocando que el disco se llene unicamente con archivos de un usuario.

Aparte, para evitar un ataque de fuerza bruta, seria necesario bloquear el numero de intentos de login, si no, es posible que si la contraseña de un usuario no es lo suficientemente robusta.

## 5-*Set up del entorno para ejecutar el script*

### 5.1-Certificados

Para utilizar el protocolo https, es necesario copiar el archivo **cert.perm** a la ruta *usr/local/share/ca-certificates*, una vez ahí, se debe modificar el nombre a **cert.crt** y actualizar la lista de certificados para que la herramienta curl reconozca el certificado 

```
$ sudo update-ca-certificates perm.crt
```

### 5.2-Modificar archivo para resolución DNS

Según el enunciado, debemos de acceder a la dirección `myserver.local:5000` la cual se traduce en `127.0.0.1:5000`, por ello es necesario modificar el archivo **/etc/hosts** añadiendo una linea con la siguente información

```
127.0.0.1   myserver.local
```

### 5.3-Configurar virtual enviroment

Para configurar automaticamente un virtual enviroment donde instalar las librerías necesarias, simplemente ejecuta el script `set-venv.sh` de la siguiente manera:

```
$ source set-venv.sh
```
De esta manera se configurará el virtual enviroment y se instalarán las librerías necesarias automáticamente.

Para desactivar el virtual enviroment, ejecuta el siguiente comando:

```
$ deactivate
```

### 5.4-Requisitos

En el caso de no utilizar el script `set-venv.sh`, será necesario instalar manualmente la librería de `flask-restful` para poder ejecutar el programa. Para ello se puede hacer uso del `requirements.txt` para instalarla.

```
$ pip install -r requirements.txt
```


## 6-Lanzamiento de pruebas automáticas

Para el lanzamiento de las pruebas automáticas es necesario tener instalado dos herramientas: **curl** y **jq**. Si no las tienes installadas puede utilizar el siguiente comando:

```
$ sudo apt-get install curl jq
```

### 6.1-Test

Los tests desarrollados para esta practica se encuentran dentro de la carpeta **/test**

Tambien será necesario dar permisos de ejecución a los archivos **.sh** almacenados en el directorio */test*

```
$ chmod +x *.sh
```

Para facilitar el lanzamiento del servidor y sus pruebas, hemos decidido generar un archivo MakeFile con las siguientes instrucciones:
1. **all** (crea el directorio *users/* y el archivo *.shadow*, ambos son necesarios para la ejecución del servidor)
2. **run** (ejecuta el servidor)
3. **test** (realiza los test de forma ordenada)
3. **clean** (elimina los rastros dejados por el programa *users/* y *.shadow*)


De cualquier forma, si el usuario desea lanzar los scripts de manera individual, tambien se viene documetnado el como lanzarlos.

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
