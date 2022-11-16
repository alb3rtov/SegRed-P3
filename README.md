# Práctica 3 - Seguridad en Redes

## Integrantes

Alberto Vázquez Martínez - Alberto.Vazquez1@alu.uclm.es

Paulino de la Fuente Lizcano - Paulino.Lafuente@alu.uclm.es

## Explicación

Este proyecto simula un servicio de almacenamiento online donde se pueden registrar diferentes usuarios, cada usuario tiene su espacio para poder subir archivos en formato ***.json**,
se dispone de un archivo llamado **.shadow** simulando el comportamiento de un entorno linux, donde se almacena el nombre de usuario, seguido de un codigo utilizado para generar el hash de la contraseña y la misma.

```
usuario:salt:hash
```

A su vez, se utilizan tokens para validar las acciones de dichos usuarios, dichas acciones son:
1. **GET** sobre un archivo
2. **POST** de un archivo
3. **PUT** de un archivo existente
4. **DELETE** un archivo

Los tokens tienen un tiempo de uso, por defecto están configurados para que duren 5 minutos, en el caso de que se desee modificar el tiempo de vida del token, tan solo hay que modificar la varibale global **MINUTES**

Para la gestión de los tokens, hemos decidio usar 2 diccionarios llamados *TOKENS_DICT* y *EXP_TOKEN*, en el primero se asocia un token a un usuario y en el otro se asocia una fecha limite para poder ser usado. En el momento en que caduca, ambos diccionarios se sincronizan para que el token expirado se elimine y se genere otro si el usuario registrado introduce bien su id de usuario y su contraseña.

Para comunicarse con el servidor, es necesario utilizar el protocolo HTTPS, ya que si se usa el protocolo HTTP es denegado.

## Certificados

Para utilizar el protocolo https, es necesario copiar el archivo **cert.perm** a la ruta *usr/local/share/ca-certificates*, una vez ahí, se debe modificar el nombre a **cert.crt** y actualizar la lista de certificados para que la herramienta curl reconozca el certificado 

```
$ sudo update-ca-certificates perm.crt
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

Según el enunciado, debemos de acceder a la dirección `myserver.local:5000` la cual se traduce en `127.0.0.1:5000`, por ello es necesario modificar el archivo **/etc/hosts** añadiendo una linea con la siguente información

```
127.0.0.1   myserver.local
```

## Requisitos

En el caso de no utilizar el script `set-venv.sh`, será necesario instalar manualmente la librería de `flask-restful` para poder ejecutar el programa. Para ello se puede hacer uso del `requirements.txt` para instalarla.

```
$ pip install -r requirements.txt
```

## Generación de token de autenticación

Para la generación del token de autenticación de usuarios hemos optado por utilizar `UUIDs` (versión 4), ya que son identificadores únicos universales y así nos aseguramos de que el token no se repita para otro usuario. 

Cuando generamos un token, almacenamos la hora de creación del token para así poder comprobar si ha caducado o no.

## Aspectos a mejorar

Es posible que si el programa es usado por muchos usuarios, sea necesario el limitar el espacio que estos pueden usar, si no, un usuario podria subir archivos muy pesados provocando que el disco se llene unicamente con archivos de un usuario.

Aparte, para evitar un ataque de fuerza bruta, seria necesario bloquear el numero de intentos de login, si no, es posible que si la contraseña de un usuario no es lo suficientemente robusta.

## Lanzamiento de pruebas automáticas

Para el lanzamiento de las pruebas automáticas es necesario tener instalado dos herramientas: **curl** y **jq**. Si no las tienes installadas puede utilizar el siguiente comando:

```
$ sudo apt-get install curl jq
```

Para lanzar cada uno de los scripts de prueba es necesario primero lanzar el servidor. Para ello, simplemente hay que ejecutar el script de python `main.py`.

```
$ python3 ./main.py
```

 Tambien será necesario dar permisos de ejecución a los archivos **.sh** almacenados en el directorio */test*


```
$ chmod +x *.sh
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
