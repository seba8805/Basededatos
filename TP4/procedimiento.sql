DELIMITER //
CREATE PROCEDURE MigrarClientes()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_NombreCompleto VARCHAR(150);
    DECLARE v_Telefono VARCHAR(20);
    DECLARE v_Direccion VARCHAR(255);
    DECLARE v_FechaRegistro DATETIME;
    
    DECLARE curClientes CURSOR FOR
        SELECT NombreCompleto, Telefono, Direccion, FechaRegistro
        FROM ClientesAntiguos;
        
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    START TRANSACTION;
    
    OPEN curClientes;

    read_loop: LOOP
        FETCH curClientes INTO v_NombreCompleto, v_Telefono, v_Direccion, v_FechaRegistro;
        
        IF done THEN
            LEAVE read_loop;
        END IF;

        SET @Nombre = SUBSTRING_INDEX(v_NombreCompleto, ' ', 1);
        SET @Apellido = SUBSTRING_INDEX(v_NombreCompleto, ' ', -1);
        
        SELECT @Nombre AS Nombre, @Apellido AS Apellido, v_Telefono AS Telefono, v_Direccion AS Direccion, DATE(v_FechaRegistro) AS FechaRegistro;

        INSERT INTO ClientesActuales (Nombre, Apellido, Telefono, Direccion, FechaRegistro)
        VALUES (@Nombre, @Apellido, v_Telefono, v_Direccion, DATE(v_FechaRegistro));
    END LOOP;
    
    CLOSE curClientes;
    COMMIT;
END //

DELIMITER ;