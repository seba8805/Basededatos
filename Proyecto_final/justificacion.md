# Justificacion del Diseño de la Base de Datos Biblioteca

## 1. Introduccion

Este diseño de base de datos tiene como objetivo proporcionar una estructura eficiente para gestionar la información de una **biblioteca**, incluyendo libros, usuarios, prestamos, pagos y multas. La base de datos sigue las **normas de normalizacion** hasta la **3NF** para eliminar redundancias y mejorar la eficiencia en las consultas y en el almacenamiento de datos.

## 2. Entidades Fuertes y Debiles

### 2.1 Entidades Fuertes
- **Usuarios**: Representa a las personas que utilizan la biblioteca. Esta entidad tiene atributos clave como `id_usuario`, `nombre`, `direccion`, `telefono`, `email` y `fecha_registro`. La entidad **Usuarios** es fuerte ya que puede existir independientemente de otras entidades.
  
- **Libros**: Representa los libros disponibles en la biblioteca. Atributos clave: `id_libro`, `titulo`, `autor`, `genero`, `estado`. Esta entidad tambien es fuerte, ya que puede existir de forma independiente a otras entidades.

- **Prestamos**: Representa los prestamos de libros que los usuarios hacen en la biblioteca. Tiene como claves foraneas el `id_usuario` y `id_libro`. La entidad **Prestamos** depende de las entidades **Usuarios** y **Libros**, por lo que es una entidad debil.

- **Pagos**: Representa los pagos realizados por los usuarios. Incluye `id_usuario`, `monto`, `fecha_pago`. Tambien depende de **Usuarios**, por lo que es una entidad débil.

- **Multas**: No esta modelada explícitamente como una entidad en este diseño, la multa es calculada a partir de la fecha de devolución real (es decir cuando finalmente el usuario devuelve el libro) y la fecha pactada del prestamo. Se gestiona como un calculo derivado, no como una entidad separada.

### 2.2 Entidades Debiles
- **Prestamos**: Como se menciono anteriormente, esta entidad depende de **Usuarios** y **Libros** para su existencia. No tiene una clave primaria independiente, sino que depende de las claves primarias de otras entidades.

- **Pagos**: Tambien es una entidad debil que depende de la entidad **Usuarios**. El pago esta asociado a un usuario y no puede existir sin un usuario.

## 3. Atributos de las Entidades

- **Usuarios**: 
  - `id_usuario`: Identificador unico.
  - `nombre`: Nombre completo del usuario.
  - `direccion`: Dirección de contacto del usuario.
  - `telefono`: Telefono de contacto.
  - `email`: Correo electrónico del usuario.
  - `fecha_registro`: Fecha de registro en el sistema.

- **Libros**:
  - `id_libro`: Identificador unico del libro.
  - `titulo`: Titulo del libro.
  - `autor`: Autor del libro.
  - `genero`: Genero del libro.
  - `estado`: Indica si el libro está "Disponible" o "Prestado".

- **Prestamos**:
  - `id_prestamo`: Identificador unico del prestamo.
  - `id_usuario`: Relacionado con la entidad **Usuarios**.
  - `id_libro`: Relacionado con la entidad **Libros**.
  - `fecha_prestamo`: Fecha en la que se realizo el préstamo.
  - `fecha_devolucion`: Fecha en la que se espera la devolucion del libro.
  - `fecha_devolucion_real`: Fecha en la que realmente el usuario devolvio el libro (para calcular multas).

- **Pagos**:
  - `id_pago`: Identificador unico del pago.
  - `id_usuario`: Relacionado con la entidad **Usuarios**.
  - `monto`: Monto del pago realizado.
  - `fecha_pago`: Fecha en la que se realizo el pago.

## 4. Relaciones y Cardinalidades

### 4.1 Relacion entre **Usuarios** y **Prestamos**
- **Cardinalidad**: Un **usuario** puede realizar multiples **prestamos**, pero un **prestamo** solo pertenece a un unico **usuario**.
  - **Relación**: 1:N (un usuario a muchos prestamos)

### 4.2 Relacion entre **Libros** y **Prestamos**
- **Cardinalidad**: Un **libro** puede ser prestado varias veces, pero cada **prestamo** se asocia a un unico **libro**.
  - **Relacion**: 1:N (un libro a muchos prestamos)

### 4.3 Relacion entre **Usuarios** y **Pagos**
- **Cardinalidad**: Un **usuario** puede hacer varios **pagos** a lo largo del tiempo, pero cada **pago** esta asociado con un unico **usuario**.
  - **Relación**: 1:N (un usuario a muchos pagos)

### 4.4 Relación entre **Libros** y **Pagos** (Indirecta)
- No hay una relación directa entre **Libros** y **Pagos**. Sin embargo, los pagos estan relacionados indirectamente a traves de la entidad **Usuarios**, ya que los pagos se hacen por usuario y pueden estar relacionados con prestamos de libros.

## 5. Normalizacion

### 5.1 Primera Forma Normal (1NF)
Para que las tablas estén en **1NF**, debemos asegurarnos de que:
- Los **atributos** de cada entidad contengan valores atomicos (no repetitivos ni compuestos).
- No haya grupos repetidos de atributos dentro de una misma entidad.

En este diseño, cada tabla tiene un conjunto único de atributos atomicos, y no existen grupos repetitivos. Por ejemplo, la tabla **Usuarios** tiene atributos como `id_usuario`, `nombre`, `direccion`, `telefono` y `email`, todos con valores atomicos y no repetidos.

### 5.2 Segunda Forma Normal (2NF)
Para que las tablas estén en **2NF**, deben cumplir las siguientes condiciones:
- Estar en **1NF**.
- No debe haber dependencias parciales, es decir, ningun atributo debe depender solo de una parte de la clave primaria.

En este diseño:
- La tabla **Prestamos** tiene como claves foráneas `id_usuario` y `id_libro`, y todos los atributos dependen completamente de esta clave compuesta. No hay dependencias parciales, ya que cada atributo esta completamente dependiente de la clave primaria compuesta.

### 5.3 Tercera Forma Normal (3NF)
Para que las tablas esten en **3NF**, deben cumplir las siguientes condiciones:
- Estar en **2NF**.
- No debe haber dependencias transitivas, es decir, los atributos no clave no deben depender de otros atributos no clave.

En este diseño:
- Las tablas no tienen dependencias transitivas. Por ejemplo, el **monto** del pago depende directamente de la relacion con el **usuario**, pero no depende de otros atributos que no sean parte de la clave primaria.

## 6. Esquema Final de la Base de Datos

El esquema final de la base de datos es el siguiente:

### Tabla: **Usuarios**
| Atributo      | Tipo       | Descripción               |
|---------------|------------|---------------------------|
| id_usuario    | INT        | Identificador unico        |
| nombre        | VARCHAR    | Nombre del usuario         |
| direccion     | VARCHAR    | Direccion del usuario      |
| telefono      | VARCHAR    | Telefono de contacto       |
| email         | VARCHAR    | Correo electronico         |
| fecha_registro| DATE       | Fecha de registro          |

### Tabla: **Libros**
| Atributo      | Tipo       | Descripcion               |
|---------------|------------|---------------------------|
| id_libro      | INT        | Identificador unico        |
| titulo        | VARCHAR    | Titulo del libro           |
| autor         | VARCHAR    | Autor del libro            |
| genero        | VARCHAR    | Géenero del libro           |
| estado        | VARCHAR    | Estado del libro (Disponible/Prestado) |

### Tabla: **Prestamos**
| Atributo           | Tipo       | Descripcion                     |
|--------------------|------------|---------------------------------|
| id_prestamo        | INT        | Identificador unico              |
| id_usuario         | INT        | Clave foranea de Usuarios        |
| id_libro           | INT        | Clave foranea de Libros          |
| fecha_prestamo     | DATE       | Fecha del prestamo               |
| fecha_devolucion   | DATE       | Fecha pactada de devolucion      |
| fecha_devolucion_real | DATE    | Fecha real de devolucion         |

### Tabla: **Pagos**
| Atributo      | Tipo       | Descripcion               |
|---------------|------------|---------------------------|
| id_pago       | INT        | Identificador unico        |
| id_usuario    | INT        | Clave foranea de Usuarios  |
| monto         | DECIMAL    | Monto del pago             |
| fecha_pago    | DATE       | Fecha del pago             |

## 7. Conclusiones

El diseño de la base de datos se ha realizado siguiendo los principios de normalización hasta la **tercera forma normal (3NF)**, lo que asegura que los datos se almacenan de manera eficiente, sin redundancias innecesarias. Ademas, las entidades, atributos y relaciones se han definido de manera clara para asegurar que el sistema de gestion de la biblioteca sea escalable y facil de mantener.
