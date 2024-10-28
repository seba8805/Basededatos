CREATE TABLE ClientesAntiguos (
    ClienteId INT PRIMARY KEY AUTO_INCREMENT,
    NombreCompleto VARCHAR(150) NOT NULL,
    Telefono VARCHAR(20),
    Direccion VARCHAR(255),
    FechaRegistro DATETIME NOT NULL
);