CREATE TABLE ClientesActuales (
    ClienteId INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(100) NOT NULL,
    Apellido VARCHAR(50) NOT NULL,
    Telefono VARCHAR(20),
    Direccion VARCHAR(255),
    FechaRegistro DATE NOT NULL
);