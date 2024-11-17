# Justificacion del Diseno de la Base de Datos para Talleres de Autos

## 1. Dependencias Funcionales (DFs)

1. **`codigoSucursal -> domicilioSucursal, telefonoSucursal`**  
   El codigo de sucursal determina de manera unica el domicilio y el telefono de la sucursal.

2. **`codigoSucursal, codigoFosa -> largoFosa, anchoFosa`**  
   La combinacion de `codigoSucursal` y `codigoFosa` determina las dimensiones de la fosa.

3. **`codigoFosa -> patenteAuto, marcaAuto, modeloAuto, dniCliente`**  
   Cada fosa tiene asociada una lista de autos que se arreglaron en ella. El codigo de la fosa determina los autos reparados, identificados por su `patenteAuto`, `marcaAuto`, `modeloAuto` y el `dniCliente` del propietario.

4. **`patenteAuto -> dniCliente, marcaAuto, modeloAuto`**  
   La patente de un auto es unica, esto permite determinar su `marcaAuto`, `modeloAuto` y el `dniCliente` del propietario.

5. **`dniCliente -> nombreCliente, celularCliente`**  
   El `dniCliente` es unico para cada cliente, por lo que podemos determinar su `nombreCliente` y `celularCliente`.

6. **`dniMecanico -> nombreMecanico, emailMecanico`**  
   El `dniMecanico` es unico para cada mecanico, lo que nos permite determinar su `nombreMecanico` y `emailMecanico`.

7. **`codigoSucursal, dniMecanico -> nombreMecanico, emailMecanico`**  
   El `codigoSucursal` y el `dniMecanico` juntos nos permiten determinar el `nombreMecanico` y `emailMecanico` de un mecanico que trabaja en esa sucursal.

## 2. Clave Candidata
La clave candidata para el esquema es la combinacion de los atributos: **(codigoSucursal, codigoFosa, patenteAuto)**

- **codigoSucursal**: Identifica de manera unica la sucursal.
- **codigoFosa**: Identifica de manera unica cada fosa dentro de la sucursal.
- **patenteAuto**: Identifica de manera unica cada auto.

Con esta combinacion, podemos identificar de manera unica cada registro en la base de datos.

## 3. Normalizacion

### 1FN: 
El esquema inicial esta en **Primera Forma Normal (1FN)**, ya que todos los atributos contienen valores atomicos, es decir, 
no hay atributos que contengan listas o valores repetidos.

### 2FN: 
En la **Segunda Forma Normal (2FN)**, se eliminaron las dependencias parciales. Esto se realizo separando los datos en tablas diferentes 
segun el tipo de dependencia, como la informacion de la sucursal, la fosa, el auto, el cliente y el mecanico.

### 3FN: 
El esquema esta en **Tercera Forma Normal (3FN)**, ya que no existen dependencias transitivas. Cada atributo no clave depende de la clave
 primaria completa.

## 4. Diseno Final en 3FN

El diseno final de la base de datos es el siguiente:

### Tablas:

1. **Sucursal**: Contiene informacion sobre cada sucursal del taller.
   - `codigoSucursal`, `domicilioSucursal`, `telefonoSucursal`.

2. **Fosa**: Contiene la informacion de las fosas asociadas a cada sucursal.
   - `codigoSucursal`, `codigoFosa`, `largoFosa`, `anchoFosa`.

3. **Auto**: Contiene los datos de los autos registrados, junto con el cliente que los posee.
   - `patenteAuto`, `marcaAuto`, `modeloAuto`, `dniCliente`.

4. **Cliente**: Contiene informacion de los clientes.
   - `dniCliente`, `nombreCliente`, `celularCliente`.

5. **Mecanico**: Contiene informacion de los mecanicos del taller.
   - `dniMecanico`, `nombreMecanico`, `emailMecanico`.

6. **Taller**: Relaciona las fosas con los autos y las sucursales.
   - `codigoSucursal`, `codigoFosa`, `patenteAuto`.

## Conclusion

El diseno de la base de datos esta normalizado hasta la **3FN**, lo que asegura la eliminacion de redundancias y 
mejora la consistencia de los datos. Las tablas estan organizadas de manera eficiente, garantizando que la base de datos sea facil 
de mantener y consultar.
