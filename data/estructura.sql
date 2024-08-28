-- AUTORES
-- Emanuel Pacheco Alberto
-- Leonel Federico Valencia Estudillo

-- ELIMINAR BASE DE DATOS

-- DROP DATABASE el_gabacho;

-- CREACION DE LA BASE DE DATOS

CREATE OR REPLACE DATABASE el_gabacho;

-- USAR LA BASE DE DATOS

USE el_gabacho;

SET GLOBAL innodb_lock_wait_timeout = 120;

-- CREACION DE LA TABLA TELEFONOSEMPRESA

CREATE TABLE telefonosEmpresa (
  idTelefono INT AUTO_INCREMENT PRIMARY KEY,
  numero VARCHAR(20) NOT NULL,
  tipo VARCHAR(20) NOT NULL
);

-- CREACION DE LA TABLA CONFIGURACION

CREATE TABLE configuracion (
  idConfiguracion INT AUTO_INCREMENT PRIMARY KEY,
  correo VARCHAR(50),
  direccion VARCHAR(100),
  encabezado VARCHAR(255),
  footer VARCHAR(255)
);

-- CREACION DE LA TABLA DIAS
CREATE TABLE horario (
  idDia INT AUTO_INCREMENT PRIMARY KEY,
  dias VARCHAR(50) NOT NULL UNIQUE,
  horaInicio VARCHAR(10) NOT NULL,
  horaFin VARCHAR(10) NOT NULL
);

-- CREACION DE LA TABLA CATEGORIAS

CREATE TABLE categorias (
  idCategoria INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL UNIQUE
);

-- CREACION DE LA TABLA UNIDAD MEDIDAS ** OCULTO ** = M/CM ó PQ/PZ

CREATE TABLE unidadMedidas (
  idUnidadMedida INT AUTO_INCREMENT PRIMARY KEY,
  tipoMedida VARCHAR(8) NOT NULL UNIQUE,
  descripcion VARCHAR(100)
);

 -- CREACION DE LA TABLA ROLES ** OCULTO **
 
CREATE TABLE roles (
	idRol INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  descripcion VARCHAR(100)
);

 -- CREACION DE LA TABLA USUARIOS **
 
 CREATE TABLE usuarios (
  idUsuario INT AUTO_INCREMENT PRIMARY KEY,
  idRol INT NOT NULL,
  nombreCompleto VARCHAR(50) NOT NULL,
  usuario VARCHAR(15) NOT NULL,
  contrasenia VARCHAR(200) NOT NULL,
  fechaCreacion TIMESTAMP default CURRENT_TIMESTAMP,
  estado BOOL DEFAULT TRUE,
  FOREIGN KEY (idRol) REFERENCES roles(idRol)
);

-- CREACION DE LA TABLA PROVEEDORES *

CREATE TABLE proveedores (
  idProveedor INT AUTO_INCREMENT PRIMARY KEY,
  empresa VARCHAR(50) NOT NULL UNIQUE,
  nombreEncargado VARCHAR(50),
  telefono VARCHAR(10),
  correo VARCHAR(50)
);

-- CREACION DE LA TABLA TIPO PAGOS ** OCULTO ** = EFECTIVO, CARJETA, TRANSFERENCIA, DEPOSITO

CREATE TABLE tipoPagos (
	idTipoPago INT AUTO_INCREMENT PRIMARY KEY,
  tipoPago VARCHAR(20) NOT NULL,
  descripcion VARCHAR(100)
);

-- CREACION DE LA TABLA CLIENTES = PUBLICO GENERAL

CREATE TABLE clientes (
	idCliente INT AUTO_INCREMENT PRIMARY KEY,
	nombre VARCHAR(30) NOT NULL UNIQUE
);

-- CREACION DE LA TABLA MARCAS MODELOS Y AÑOS

-- CREACION DE LA TABLA MARCAS

CREATE TABLE marcas (
	idMarca INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(45) NOT NULL UNIQUE,
  urlLogo VARCHAR(300)
);

-- CREACION DE LA TABLA MODELOS

CREATE TABLE modelos (
  idModelo INT AUTO_INCREMENT PRIMARY KEY,
  idMarca INT NOT NULL,
  nombre VARCHAR(50) NOT NULL,
  FOREIGN KEY (idMarca) REFERENCES marcas(idMarca)
);

-- CREACION DE LA TABLA AÑOS

CREATE TABLE anios (
  idAnio INT AUTO_INCREMENT PRIMARY KEY,
  anioInicio INT UNSIGNED NOT NULL,
  anioFin INT UNSIGNED NOT NULL,
  anioTodo BOOL DEFAULT FALSE NOT NULL,
  UNIQUE (anioInicio, anioFin)
);

-- CREACION DE LA TABLA RELACION MODELO AÑOS "RELACION TABLA MODELOS Y AÑO MODELOS"

CREATE TABLE modeloAnios (
	idModeloAnio INT AUTO_INCREMENT PRIMARY KEY,
	idModelo INT NOT NULL,
	idAnio INT NOT NULL,
	FOREIGN KEY (idModelo) REFERENCES modelos(idModelo) ON DELETE CASCADE,
	FOREIGN KEY (idAnio) REFERENCES anios(idAnio)
);

-- CREACION DE LA TABLA INVENTARIO AUTOPARTES
CREATE TABLE inventario (
	idInventario INT AUTO_INCREMENT PRIMARY KEY,
	idCategoria INT DEFAULT NULL,
	idUnidadMedida INT NOT NULL,
   codigoBarras VARCHAR(50) NOT NULL UNIQUE,
   nombre VARCHAR(100) NOT NULL,
   descripcion VARCHAR(150) NOT NULL,
   cantidadActual FLOAT UNSIGNED DEFAULT 0 NOT NULL,
   cantidadMinima FLOAT UNSIGNED DEFAULT 1 NOT NULL,
   precioCompra FLOAT UNSIGNED DEFAULT 0.00 NOT NULL,
   mayoreo FLOAT UNSIGNED DEFAULT 0.00 NOT NULL,
   menudeo FLOAT UNSIGNED DEFAULT 0.00 NOT NULL,
   colocado FLOAT UNSIGNED DEFAULT 0.00 NOT NULL,
   estado BOOL DEFAULT TRUE,
   FOREIGN KEY (idCategoria) REFERENCES categorias(idCategoria) ON DELETE SET NULL,
   FOREIGN KEY (idUnidadMedida) REFERENCES unidadMedidas(idUnidadMedida)
   -- ON UPDATE CASCADE  -- Permite el UPDATE en idUnidadMedida en inventario
   --   ON DELETE RESTRICT -- No permite DELETE en unidadMedidas involuntariamente
);

-- CREACION DE LA TABLA IMAGENES "RELACION TABLA IMAGENES CON INVENTARIO"

CREATE TABLE imagenes (
    idImagenes INT AUTO_INCREMENT PRIMARY KEY,
    idInventario INT NOT NULL,
    imgRepresentativa BOOL DEFAULT FALSE,
    img2 BOOL DEFAULT FALSE,
    img3 BOOL DEFAULT FALSE,
    img4 BOOL DEFAULT FALSE,
    img5 BOOL DEFAULT FALSE,
    FOREIGN KEY (idInventario) REFERENCES inventario(idInventario)
);

-- CREACION DE LA TABLA RELACION MODELO AUTOPARTES "RELACION TABLA MODELO AÑO Y INVENTARIO AUTOPARTE"

CREATE TABLE modeloAutopartes (
	idModeloAutoparte INT AUTO_INCREMENT PRIMARY KEY,
	idModeloAnio INT NOT NULL,
	idInventario INT NOT NULL,
	FOREIGN KEY (idModeloAnio) REFERENCES modeloAnios(idModeloAnio) ON DELETE CASCADE,
	FOREIGN KEY (idInventario) REFERENCES inventario(idInventario)
);

-- CREACION DE LA TABLA RELACION PROVEEDOR PRODUCTOS "RELACION TABLA PROVEEDORES Y INVENTARIO AUTOPARTES"

CREATE TABLE proveedorProductos (
  idProveedorProducto INT AUTO_INCREMENT PRIMARY KEY,
  idProveedor INT NOT NULL,
  idInventario INT NOT NULL,
  FOREIGN KEY (idProveedor) REFERENCES proveedores(idProveedor) ON DELETE CASCADE,
  FOREIGN KEY (idInventario) REFERENCES inventario(idInventario)
);

-- CREACION DE LA TABLA RELACION ENTRADA PRODUCTOS "RELACION TABLA USUARIOS Y INVENTARIO AUTOPARTES"

CREATE TABLE entradaProductos (
  idEntradaProducto INT AUTO_INCREMENT PRIMARY KEY,
  idUsuario INT NOT NULL,
  idInventario INT NOT NULL,
  cantidadNueva FLOAT UNSIGNED NOT NULL,
  precioCompra FLOAT UNSIGNED NOT NULL,
  fechaEntrada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (idUsuario) REFERENCES usuarios(idUsuario),
  FOREIGN KEY (idInventario) REFERENCES inventario(idInventario)
);

-- CREACION DE LA TABLA RELACION REGISTRO PRODUCTOS "RELACION TABLA USUARIOS Y INVENTARIO AUTOPARTES"

CREATE TABLE registroProductos (
  idRegistroProducto INT AUTO_INCREMENT PRIMARY KEY,
  idInventario INT NOT NULL,
  idUsuarioRegistro INT NOT NULL,
  fechaCreacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  idUsuarioElimino INT DEFAULT NULL,
  fechaElimino TIMESTAMP DEFAULT NULL,
  FOREIGN KEY (idInventario) REFERENCES inventario(idInventario),
  FOREIGN KEY (idUsuarioRegistro) REFERENCES usuarios(idUsuario)
  );

-- CREACION DE LA TABLA RELACION VENTAS "RELACION TABLA USUARIO Y CLIENTE" 

CREATE TABLE ventas (
  idVenta INT AUTO_INCREMENT PRIMARY KEY,
  idUsuario INT NOT NULL,
  idCliente INT NOT NULL,
  montoTotal FLOAT UNSIGNED NOT NULL,
  recibioDinero FLOAT UNSIGNED NOT NULL,
  folioTicket VARCHAR(50) NOT NULL,
  imprimioTicket BOOL NOT NULL,
  fechaVenta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (idUsuario) REFERENCES usuarios(idUsuario),
  FOREIGN KEY (idCliente) REFERENCES clientes(idCliente)
);

-- CREACION DE LA TABLA RELACION PAGO VENTAS "RELACION TABLA VENTAS Y TIPO PAGOS"

CREATE TABLE pagoVenta (
  idPagoVenta INT AUTO_INCREMENT PRIMARY KEY,
  idVenta INT NOT NULL,
  idTipoPago INT NOT NULL,
  referenciaUnica VARCHAR(50),
  FOREIGN KEY (idVenta) REFERENCES ventas(idVenta),
  FOREIGN KEY (idTipoPago) REFERENCES tipoPagos(idTipoPago)
);

-- CREACION DE LA TABLA RELACION VENTA PRODUCTOS "RELACION TABLA INVENTARIO AUTOPARTES Y VENTAS"

CREATE TABLE ventaProductos (
  idVentaProducto INT AUTO_INCREMENT PRIMARY KEY,
  idVenta INT NOT NULL,
  idInventario INT NOT NULL,
  cantidad FLOAT UNSIGNED NOT NULL,
  tipoVenta VARCHAR(50) NOT NULL,
  precioVenta FLOAT UNSIGNED NOT NULL,
  subtotal FLOAT UNSIGNED NOT NULL,
  FOREIGN KEY (idVenta) REFERENCES ventas(idVenta),
  FOREIGN KEY (idInventario) REFERENCES inventario(idInventario)
);

-- CREACION DE LA TABLA BITACORAVENTAS
CREATE TABLE BitacoraVentas (
  idUsuario INT,
  idVenta INT NOT NULL,
  idInventario INT NOT NULL,
  cantidadProducto FLOAT UNSIGNED NOT NULL,
  precioVenta FLOAT UNSIGNED NOT NULL,
  montoTotal FLOAT UNSIGNED NOT NULL,
  fechaActualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TIGGERS Y PROCEDIMIENTOS PARA LA BASE DE DATOS

--------------------------------------------------------------------------------------------------------------------------------------------
-- procedimientos para insertar registros --------------------------------------------------------------------------------------------

DELIMITER $$

CREATE PROCEDURE proc_insertar_producto(
    IN p_idCategoria INT,
    IN p_idUnidadMedida INT,
    IN p_codigoBarras VARCHAR(50),
    IN p_nombre VARCHAR(100),
    IN p_descripcion VARCHAR(150),
    IN p_cantidadActual FLOAT,
    IN p_cantidadMinima FLOAT,
    IN p_precioCompra FLOAT,
    IN p_mayoreo FLOAT,
    IN p_menudeo FLOAT,
    IN p_colocado FLOAT,
    IN p_idProveedor INT,
    IN p_idUsuario INT,
    OUT p_idInventario INT
)
BEGIN
    -- Inicializar el parámetro de salida a 0
    SET p_idInventario = 0;

    -- Verificar si la categoría existe
    IF NOT EXISTS (SELECT 1 FROM categorias WHERE idCategoria = p_idCategoria) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La categoría especificada no existe.';
    
    -- Verificar si la unidad de medida existe
    ELSEIF NOT EXISTS (SELECT 1 FROM unidadMedidas WHERE idUnidadMedida = p_idUnidadMedida) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La unidad de medida especificada no existe.';
    
    -- Verificar si el proveedor existe
    ELSEIF NOT EXISTS (SELECT 1 FROM proveedores WHERE idProveedor = p_idProveedor) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El proveedor especificado no existe.';
    
    -- Verificar si el usuario existe
    ELSEIF NOT EXISTS (SELECT 1 FROM usuarios WHERE idUsuario = p_idUsuario) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El usuario especificado no existe.';
    
    -- Verificar si el código de barras ya existe
    ELSEIF EXISTS (SELECT 1 FROM inventario WHERE codigoBarras = p_codigoBarras) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El código de barras ya existe.';
    
    ELSE
        -- Insertar el nuevo producto en inventario
        INSERT INTO inventario (idCategoria, idUnidadMedida, codigoBarras, nombre, descripcion, cantidadActual, cantidadMinima, precioCompra, mayoreo, menudeo, colocado)
        VALUES (p_idCategoria, p_idUnidadMedida, p_codigoBarras, p_nombre, p_descripcion, p_cantidadActual, p_cantidadMinima, p_precioCompra, p_mayoreo, p_menudeo, p_colocado);

        -- Obtener el idInventario recién insertado
        SET p_idInventario = LAST_INSERT_ID();

        -- Insertar en proveedorProductos
        INSERT INTO proveedorProductos (idProveedor, idInventario)
        VALUES (p_idProveedor, p_idInventario);

        -- Insertar en registroProductos
        INSERT INTO registroProductos (idInventario, idUsuarioRegistro)
        VALUES (p_idInventario, p_idUsuario);
    END IF;
END $$

DELIMITER ;

----------------------------
----------------------------

DELIMITER $$

CREATE OR REPLACE PROCEDURE proc_inserta_img_producto(
    IN p_idInventario INT,
    IN p_imagenes TEXT
)
BEGIN
    DECLARE imgRepresentativa BOOL;
    DECLARE img2 BOOL;
    DECLARE img3 BOOL;
    DECLARE img4 BOOL;
    DECLARE img5 BOOL;

    -- Verificar si el producto existe
    IF NOT EXISTS (SELECT 1 FROM inventario WHERE idInventario = p_idInventario) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El producto con el ID especificado no existe.';
    ELSE
        -- Extraer valores booleanos de la cadena p_imagenes
        SET imgRepresentativa = TRIM(SUBSTRING_INDEX(p_imagenes, ',', 1)) = 'TRUE';
        SET img2 = TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(p_imagenes, ',', 2), ',', -1)) = 'TRUE';
        SET img3 = TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(p_imagenes, ',', 3), ',', -1)) = 'TRUE';
        SET img4 = TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(p_imagenes, ',', 4), ',', -1)) = 'TRUE';
        SET img5 = TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(p_imagenes, ',', 5), ',', -1)) = 'TRUE';

        -- Insertar imágenes relacionadas con el producto
        INSERT INTO imagenes (idInventario, imgRepresentativa, img2, img3, img4, img5)
        VALUES (p_idInventario, imgRepresentativa, img2, img3, img4, img5);
    END IF;
END $$

DELIMITER ;

------------------------------------------
------------------------------------------
-- Procedimiento para insertar modelos a productos
DELIMITER $$

CREATE PROCEDURE proc_insertar_modelos(
    IN p_idModelo INT,
    IN p_anioInicio INT,
    IN p_anioFin INT,
    IN p_anioTodo BOOL
)
BEGIN
    DECLARE p_idAnio INT DEFAULT NULL;
    DECLARE p_idModeloAnio INT DEFAULT NULL;

    -- Verificar si el modelo existe
    IF NOT EXISTS (SELECT 1 FROM modelos WHERE idModelo = p_idModelo) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El modelo con el ID especificado no existe.';
    END IF;

    -- Manejo de años
    IF p_anioTodo = FALSE THEN
        -- Buscar el rango de años
        SELECT idAnio INTO p_idAnio
        FROM anios
        WHERE anioInicio = p_anioInicio AND anioFin = p_anioFin;
        
        -- Si no existe, insertar nuevo rango de años
        IF p_idAnio IS NULL THEN
            INSERT INTO anios (anioInicio, anioFin, anioTodo)
            VALUES (p_anioInicio, p_anioFin, FALSE);
            SET p_idAnio = LAST_INSERT_ID();
        END IF;
    ELSE
        -- Buscar o insertar registro para todos los años
        SELECT idAnio INTO p_idAnio
        FROM anios
        WHERE anioInicio = 0 AND anioFin = 0 AND anioTodo = TRUE;
        
        -- Si no existe, insertar nuevo registro para todos los años
        IF p_idAnio IS NULL THEN
            INSERT INTO anios (anioInicio, anioFin, anioTodo)
            VALUES (0, 0, TRUE);
            SET p_idAnio = LAST_INSERT_ID();
        END IF;
    END IF;

    -- Verificar la relación entre modelo y año
    SELECT idModeloAnio INTO p_idModeloAnio
    FROM modeloAnios
    WHERE idModelo = p_idModelo AND idAnio = p_idAnio;
    
    -- Si no existe, insertar nueva relación modelo-año
    IF p_idModeloAnio IS NULL THEN
        INSERT INTO modeloAnios (idModelo, idAnio)
        VALUES (p_idModelo, p_idAnio);
    END IF;

END $$

DELIMITER ;


------------------------------------------
------------------------------------------
-- Procedimiento para relacionar un producto con un modeloanio
DELIMITER $$

CREATE PROCEDURE proc_relate_producto_modeloanios(
    IN p_idInventario INT,
    IN p_modelosAnios TEXT
)
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE modeloAnioID INT;
    DECLARE cur CURSOR FOR 
        SELECT TRIM(CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(p_modelosAnios, ',', numbers.n), ',', -1) AS UNSIGNED)) AS modeloAnioID
        FROM 
            (SELECT 1 n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 
             UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 
             UNION ALL SELECT 9 UNION ALL SELECT 10) numbers
        WHERE numbers.n <= 1 + (LENGTH(p_modelosAnios) - LENGTH(REPLACE(p_modelosAnios, ',', ''))) / LENGTH(',');

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Verificar si el idInventario existe
    IF NOT EXISTS (SELECT 1 FROM inventario WHERE idInventario = p_idInventario) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El idInventario especificado no existe.';
    ELSE
        OPEN cur;

        read_loop: LOOP
            FETCH cur INTO modeloAnioID;
            IF done THEN
                LEAVE read_loop;
            END IF;

            -- Verificar si el idModeloAnio existe
            IF NOT EXISTS (SELECT 1 FROM modeloAnios WHERE idModeloAnio = modeloAnioID) THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El idModeloAnio con el ID especificado no existe.';
            ELSE
                -- Verificar si la relación ya existe
                IF NOT EXISTS (SELECT 1 FROM modeloAutopartes WHERE idModeloAnio = modeloAnioID AND idInventario = p_idInventario) THEN
                    -- Insertar la relación modeloAnio con el producto
                    INSERT INTO modeloAutopartes (idModeloAnio, idInventario)
                    VALUES (modeloAnioID, p_idInventario);
                END IF;
            END IF;

        END LOOP;

        CLOSE cur;
    END IF;

END $$

DELIMITER ;


-- ------------------------------------------------------------------------------------------------------------------------------
-- -----------------------------------------------------------------------------------------------------------------------------------

-- Editar un producto

DELIMITER $$

CREATE PROCEDURE proc_actualizar_producto_con_comparacion(
    IN p_idInventario INT, -- ID DEL PRODUCTO INVENTARIO
    IN p_idCategoria INT, -- CATEGORIA
    IN p_idUnidadMedida INT, -- UNIDAD DE MEDIDA
    IN p_nombre VARCHAR(100),
    IN p_descripcion VARCHAR(150),
    IN p_cantidadActual FLOAT,
    IN p_cantidadMinima FLOAT,
    IN p_precioCompra FLOAT,
    IN p_mayoreo FLOAT,
    IN p_menudeo FLOAT,
    IN p_colocado FLOAT,
    IN p_idProveedor INT -- PROVEEDOR	
)
BEGIN
    DECLARE v_idCategoria INT;
    DECLARE v_idUnidadMedida INT;
    DECLARE v_nombre VARCHAR(100);
    DECLARE v_descripcion VARCHAR(150);
    DECLARE v_cantidadActual FLOAT;
    DECLARE v_cantidadMinima FLOAT;
    DECLARE v_precioCompra FLOAT;
    DECLARE v_mayoreo FLOAT;
    DECLARE v_menudeo FLOAT;
    DECLARE v_colocado FLOAT;

    -- Verificar si el producto existe y obtener los valores actuales
    IF NOT EXISTS (SELECT 1 FROM inventario WHERE idInventario = p_idInventario) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El producto con el ID especificado no existe.';
    ELSE
        -- Obtener los valores actuales del producto
        SELECT idCategoria, idUnidadMedida, nombre, descripcion, cantidadActual, cantidadMinima, 
               precioCompra, mayoreo, menudeo, colocado
        INTO v_idCategoria, v_idUnidadMedida, v_nombre, v_descripcion, v_cantidadActual, 
             v_cantidadMinima, v_precioCompra, v_mayoreo, v_menudeo, v_colocado
        FROM inventario
        WHERE idInventario = p_idInventario;

        -- Solo actualizar los campos que hayan cambiado
        IF p_idCategoria != v_idCategoria OR p_idUnidadMedida != v_idUnidadMedida OR p_nombre != v_nombre
           OR p_descripcion != v_descripcion OR p_cantidadActual != v_cantidadActual OR p_cantidadMinima != v_cantidadMinima
           OR p_precioCompra != v_precioCompra OR p_mayoreo != v_mayoreo OR p_menudeo != v_menudeo OR p_colocado != v_colocado THEN
            UPDATE inventario
            SET idCategoria = p_idCategoria,
                idUnidadMedida = p_idUnidadMedida,
                nombre = p_nombre,
                descripcion = p_descripcion,
                cantidadActual = p_cantidadActual,
                cantidadMinima = p_cantidadMinima,
                precioCompra = p_precioCompra,
                mayoreo = p_mayoreo,
                menudeo = p_menudeo,
                colocado = p_colocado
            WHERE idInventario = p_idInventario;
        END IF;

        -- Verificar si el proveedor ha cambiado
        IF NOT EXISTS (SELECT 1 FROM proveedorProductos WHERE idProveedor = p_idProveedor AND idInventario = p_idInventario) THEN
            -- Eliminar antiguo proveedor (si existe)
            DELETE FROM proveedorProductos
            WHERE idInventario = p_idInventario;

            -- Insertar nuevo proveedor
            INSERT INTO proveedorProductos (idProveedor, idInventario)
            VALUES (p_idProveedor, p_idInventario);
        END IF;
    END IF;
END $$

DELIMITER ;

-----------------------------------------
-----------------------------------------

-- Ediar un producto en imagenes
DELIMITER $$

CREATE PROCEDURE proc_actualizar_imagenes_producto(
    IN p_idInventario INT,       -- ID DEL PRODUCTO INVENTARIO
    IN p_imgRepresentativa BOOL, -- IMAGEN REPRESENTATIVA
    IN p_img2 BOOL,              -- IMAGEN 2
    IN p_img3 BOOL,              -- IMAGEN 3
    IN p_img4 BOOL,              -- IMAGEN 4
    IN p_img5 BOOL               -- IMAGEN 5
)
BEGIN
    -- Verificar si el producto existe en la tabla inventario
    IF NOT EXISTS (SELECT 1 FROM inventario WHERE idInventario = p_idInventario) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El producto con el ID especificado no existe.';
    ELSE
        -- Verificar si ya existen imágenes para el producto
        IF EXISTS (SELECT 1 FROM imagenes WHERE idInventario = p_idInventario) THEN
            -- Actualizar las imágenes existentes
            UPDATE imagenes
            SET imgRepresentativa = p_imgRepresentativa,
                img2 = p_img2,
                img3 = p_img3,
                img4 = p_img4,
                img5 = p_img5
            WHERE idInventario = p_idInventario;
        ELSE
            -- Insertar nuevas imágenes si no existen previamente
            INSERT INTO imagenes (idInventario, imgRepresentativa, img2, img3, img4, img5)
            VALUES (p_idInventario, p_imgRepresentativa, p_img2, p_img3, p_img4, p_img5);
        END IF;
    END IF;
END $$

DELIMITER ;

------------------------------------------
------------------------------------------
-- Editar relacion modeloautoparte

DELIMITER $$

CREATE PROCEDURE proc_editar_producto_modeloanios(
    IN p_idInventario INT,
    IN p_listaActualModelosAnios TEXT, -- Lista actual de modeloAnios del producto, separados por comas
    IN p_nuevaListaModelosAnios TEXT   -- Nueva lista de modeloAnios para el producto, separados por comas
)
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE modeloAnioID INT;

    -- Cursor para recorrer la nueva lista de modelosAnios
    DECLARE cur CURSOR FOR 
        SELECT TRIM(CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(p_nuevaListaModelosAnios, ',', numbers.n), ',', -1) AS UNSIGNED)) AS modeloAnioID
        FROM 
            (SELECT 1 n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 
             UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 
             UNION ALL SELECT 9 UNION ALL SELECT 10) numbers
        WHERE numbers.n <= 1 + (LENGTH(p_nuevaListaModelosAnios) - LENGTH(REPLACE(p_nuevaListaModelosAnios, ',', ''))) / LENGTH(',');

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Identificar las relaciones que se deben eliminar (presentes en la lista actual pero no en la nueva)
    DELETE FROM modeloAutopartes
    WHERE idInventario = p_idInventario
    AND idModeloAnio NOT IN (
        SELECT TRIM(CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(p_nuevaListaModelosAnios, ',', numbers.n), ',', -1) AS UNSIGNED)) AS modeloAnioID
        FROM 
            (SELECT 1 n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 
             UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 
             UNION ALL SELECT 9 UNION ALL SELECT 10) numbers
        WHERE numbers.n <= 1 + (LENGTH(p_nuevaListaModelosAnios) - LENGTH(REPLACE(p_nuevaListaModelosAnios, ',', ''))) / LENGTH(',')
    );

    -- Abrir el cursor para insertar las nuevas relaciones
    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO modeloAnioID;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Insertar la relación si no existe
        IF NOT EXISTS (SELECT 1 FROM modeloAutopartes WHERE idInventario = p_idInventario AND idModeloAnio = modeloAnioID) THEN
            INSERT INTO modeloAutopartes (idModeloAnio, idInventario)
            VALUES (modeloAnioID, p_idInventario);
        END IF;

    END LOOP;

    CLOSE cur;

END $$

DELIMITER ;


----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------


-- Este procedimiento asegurará que un producto solo se elimine físicamente si no tiene ninguna relación en ventaProductos, 
-- mientras que en caso contrario, simplemente se deshabilitará (estado = FALSE) y se registrará la acción en registroProductos.
DELIMITER //

CREATE PROCEDURE proc_eliminar_producto (
    IN p_idInventario INT,
    IN p_idUsuario INT
)
BEGIN
    DECLARE v_countVP INT;
    DECLARE v_countEP INT;

    -- Verificar si el producto tiene relaciones en ventaProductos
    SELECT COUNT(*)
    INTO v_countVP
    FROM ventaProductos
    WHERE idInventario = p_idInventario;

    -- Verificar si el producto tiene relaciones en entradaProductos
    SELECT COUNT(*)
    INTO v_countEP
    FROM entradaProductos
    WHERE idInventario = p_idInventario;

    -- Si no hay relaciones en ambas tablas, eliminar el producto
    IF v_countVP = 0 AND v_countEP = 0 THEN
        DELETE FROM inventario
        WHERE idInventario = p_idInventario;
    ELSE
        -- Actualizar el estado del producto a FALSE en inventario
        UPDATE inventario
        SET estado = FALSE
        WHERE idInventario = p_idInventario;

        -- Actualizar el idUsuarioElimino y fechaElimino en registroProductos
        UPDATE registroProductos
        SET idUsuarioElimino = p_idUsuario,
            fechaElimino = NOW()
        WHERE idInventario = p_idInventario;
    END IF;
END //

DELIMITER ;

-- -------------------------------------------------------------------------------------------------------------------------------------------------
-- -------------------------------------------------------------------------------------------------------------------------------------------------

DELIMITER //

CREATE PROCEDURE proc_reactivar_producto (
    IN p_idInventario INT
)
BEGIN
    -- Verificar si el producto existe
    IF NOT EXISTS (SELECT 1 FROM inventario WHERE idInventario = p_idInventario) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El producto con el ID especificado no existe.';
    ELSE
        -- Verificar si el producto está en estado FALSE
        IF EXISTS (SELECT 1 FROM inventario WHERE idInventario = p_idInventario AND estado = FALSE) THEN
            -- Restaurar el estado del producto a TRUE
            UPDATE inventario
            SET estado = TRUE
            WHERE idInventario = p_idInventario;

            -- Limpiar los campos idUsuarioElimino y fechaElimino en registroProductos
            UPDATE registroProductos
            SET idUsuarioElimino = NULL,
                fechaElimino = NULL
            WHERE idInventario = p_idInventario;
        ELSE
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El producto no está en estado eliminado.';
        END IF;
    END IF;
END //

DELIMITER ;


-- -------------------------------------------------------------------------------------------------------------------------------------------------
-- -------------------------------------------------------------------------------------------------------------------------------------------------


-- ventas Paso 1: Crear una Venta
DELIMITER //

CREATE OR REPLACE PROCEDURE proc_crear_venta (
    IN p_idUsuario INT,
    IN p_idCliente INT,
    OUT p_v_idVenta INT
)
BEGIN
    INSERT INTO ventas (idUsuario, idCliente, montoTotal, recibioDinero, folioTicket, imprimioTicket)
    VALUES (p_idUsuario, p_idCliente, 0, 0, '', FALSE);
    SET p_v_idVenta = LAST_INSERT_ID();
END //

DELIMITER ;

-- ventas Paso 2: Agregar Producto a la Venta
DELIMITER //

CREATE OR REPLACE PROCEDURE proc_agregar_producto_venta (
    IN p_idVenta INT,
    IN p_idInventario INT,
    IN p_cantidad FLOAT,
    IN p_tipoVenta VARCHAR(50),
    IN p_precioVenta FLOAT,
    IN p_subtotal FLOAT
)
BEGIN
    INSERT INTO ventaProductos (idVenta, idInventario, cantidad, tipoVenta, precioVenta, subtotal)
    VALUES (p_idVenta, p_idInventario, p_cantidad, p_tipoVenta, p_precioVenta, p_subtotal);
    
    -- Actualizar la catidad de cada producto
    UPDATE inventario
    SET cantidadActual = cantidadActual - p_cantidad
    WHERE idInventario = p_idInventario;
END //
	
DELIMITER ;

-- ventas Paso 3: Finalizar la Venta
DELIMITER //

CREATE OR REPLACE PROCEDURE proc_finalizar_venta (
    IN p_idVenta INT,
    IN p_montoTotal FLOAT,
    IN p_recibioDinero FLOAT,
    IN p_folioTicket VARCHAR(50),
    IN p_imprimioTicket BOOL,
    IN p_idTipoPago INT,
    IN p_referenciaUnica VARCHAR(50)
)
BEGIN
    -- Actualizar el registro de la venta con el monto total y otros detalles
    UPDATE ventas
    SET montoTotal = p_montoTotal,
        recibioDinero = p_recibioDinero,
        folioTicket = p_folioTicket,
        imprimioTicket = p_imprimioTicket
    WHERE idVenta = p_idVenta;

    -- Registrar el pago en la tabla pagoVenta
    INSERT INTO pagoVenta (idVenta, idTipoPago, referenciaUnica)
    VALUES (p_idVenta, p_idTipoPago, p_referenciaUnica);
END //

DELIMITER ;


-- Procedimiento Almacenado para Manejar Devoluciones
DELIMITER //

CREATE OR REPLACE PROCEDURE proc_devolver_venta (
    IN p_idVenta INT
)
BEGIN
    DECLARE v_idInventario INT;
    DECLARE v_cantidad FLOAT;
    DECLARE done INT DEFAULT FALSE;
    -- Cursor para iterar sobre los productos en la venta
    DECLARE cur CURSOR FOR
    SELECT idInventario, cantidad
    FROM ventaProductos
    WHERE idVenta = p_idVenta;

    -- Handler para el final del cursor
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Abrir el cursor
    OPEN cur;
    
    read_loop: LOOP
        FETCH cur INTO v_idInventario, v_cantidad;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Actualizar la cantidad en el inventario
        UPDATE inventario
        SET cantidadActual = cantidadActual + v_cantidad
        WHERE idInventario = v_idInventario;

        -- eliminar los productos devueltos
        DELETE FROM ventaProductos
        WHERE idVenta = p_idVenta AND idInventario = v_idInventario;
    END LOOP;
    
     -- Cerrar el cursor
    CLOSE cur;
    
    -- Eliminar el pagoVenta relacionado
    DELETE FROM pagoVenta WHERE idVenta = p_idVenta;
    DELETE FROM ventas WHERE idVenta = p_idVenta;

END //

DELIMITER ;


-- Procedimiento Almacenado para Manejar Devoluciones Parciales
DELIMITER //

CREATE OR REPLACE PROCEDURE proc_devolver_producto (
    IN p_idVenta INT,
    IN p_idVentaProducto INT
)
BEGIN
	DECLARE p_idInventario INT;
	DECLARE p_cantidadDevuelta INT;
	DECLARE p_cantidadProductos INT;

	SELECT idInventario INTO p_idInventario FROM ventaProductos WHERE idVentaProducto = p_idVentaProducto; 
	SELECT cantidad INTO p_cantidadDevuelta FROM ventaProductos WHERE idVentaProducto = p_idVentaProducto; 
	
    -- Eliminar producto en ventaProductos
    DELETE FROM ventaProductos
    WHERE idVenta = p_idVenta AND idVentaProducto = p_idVentaProducto;
    
   UPDATE inventario
   SET cantidadActual = cantidadActual + p_cantidadDevuelta,
      estado = TRUE
   WHERE idInventario = p_idInventario;

    -- Verificar la cantidad de productos en la venta
    SELECT COUNT(*) INTO p_cantidadProductos FROM ventaProductos WHERE idVenta = p_idVenta;

    IF p_cantidadProductos = 0 THEN
        -- Si no hay más productos en la venta, eliminar la venta
        DELETE FROM pagoVenta WHERE idVenta = p_idVenta;
        DELETE FROM ventas WHERE idVenta = p_idVenta;
    ELSE
        -- Actualizar el montoTotal de la venta
        UPDATE ventas v
        JOIN (
            SELECT idVenta, SUM(subtotal) AS nuevoMontoTotal
            FROM ventaProductos
            WHERE idVenta = p_idVenta
            GROUP BY idVenta
        ) vp ON v.idVenta = vp.idVenta
        SET v.montoTotal = vp.nuevoMontoTotal
        WHERE v.idVenta = p_idVenta;
    END IF;
END //

DELIMITER ;

-- Procedimiento Almacenado para Manejar Devoluciones Parciales
DELIMITER //

CREATE OR REPLACE PROCEDURE proc_modificar_venta_producto (
    IN p_idVenta INT,
    IN p_idVentaProducto INT,
    IN p_tipoVenta VARCHAR(50),
    IN p_cantidad FLOAT,
    IN p_precioActualizado FLOAT
)
BEGIN
	DECLARE p_idInventario INT;
	DECLARE v_cantidadOriginal FLOAT;
   DECLARE v_existenciasActual FLOAT;
   DECLARE v_existenciasActualizado FLOAT;
	
	SELECT idInventario INTO p_idInventario FROM ventaProductos WHERE idVentaProducto = p_idVentaProducto; 
   SELECT cantidadActual INTO v_existenciasActual FROM inventario WHERE idInventario = p_idInventario;
	
   -- Obtener la cantidad original del producto en la venta
   SELECT cantidad INTO v_cantidadOriginal
   FROM ventaProductos
   WHERE idVenta = p_idVenta AND idVentaProducto = p_idVentaProducto;

    -- Validar que la cantidad devuelta no sea mayor que la cantidad original
   IF p_cantidad > v_cantidadOriginal THEN
      SET v_existenciasActualizado = v_existenciasActual - (p_cantidad - v_cantidadOriginal);
   ELSE
   	SET v_existenciasActualizado = v_existenciasActual + (v_cantidadOriginal - p_cantidad);
   END IF;

    -- Actualizar la cantidad en ventaProductos
    UPDATE ventaProductos
    SET cantidad = p_cantidad, 
      tipoVenta = p_tipoVenta,
    	precioVenta = p_precioActualizado,
      subtotal = cantidad * precioVenta
    WHERE idVenta = p_idVenta AND idVentaProducto = p_idVentaProducto;
   
   -- Actualizar la cantidad en el inventario
   UPDATE inventario
   SET cantidadActual = v_existenciasActualizado
   WHERE idInventario = p_idInventario;
    
	 -- Verificar si toda la cantidad del producto ha sido devuelta
   IF p_cantidad = 0 THEN
      DELETE FROM ventaProductos
    	WHERE idVenta = p_idVenta AND idVentaProducto = p_idVentaProducto;
  		
  		DELETE FROM pagoVenta WHERE idVenta = p_idVenta;
      DELETE FROM ventas WHERE idVenta = p_idVenta;
   ELSE
   	-- Actualizar el montoTotal de la venta
    	UPDATE ventas v
    	JOIN (
        SELECT idVenta, SUM(subtotal) AS nuevoMontoTotal
        FROM ventaProductos
        WHERE idVenta = p_idVenta
        GROUP BY idVenta
    	) vp ON v.idVenta = vp.idVenta
    	SET v.montoTotal = vp.nuevoMontoTotal
    	WHERE v.idVenta = p_idVenta;
   END IF;
END //

DELIMITER ;

-- procedimiento almacenado que inserte datos en la tabla entradaProductos y actualice la tabla inventario con los precios de compra, mayoreo, menudeo y colocado
DELIMITER //

CREATE PROCEDURE proc_insertar_entrada_producto(
    IN p_idUsuario INT,
    IN p_idInventario INT,
    IN p_cantidadNueva FLOAT,
    IN p_precioCompra FLOAT,
    IN p_mayoreo FLOAT,
    IN p_menudeo FLOAT,
    IN p_colocado FLOAT
)
BEGIN
    -- Insertar el nuevo registro en entradaProductos
    INSERT INTO entradaProductos (idUsuario, idInventario, cantidadNueva, precioCompra)
    VALUES (p_idUsuario, p_idInventario, p_cantidadNueva, p_precioCompra);
    
    -- Actualizar la tabla inventario con los nuevos precios y cantidad actual
    UPDATE inventario
    SET 
        cantidadActual = cantidadActual + p_cantidadNueva,
        precioCompra = p_precioCompra,
        mayoreo = p_mayoreo,
        menudeo = p_menudeo,
        colocado = p_colocado
    WHERE idInventario = p_idInventario;
END //

DELIMITER ;

-- trigger para cuando se elimina un registro en la tabla ventaProductos
DELIMITER //

CREATE TRIGGER after_ventaProductos_delete
AFTER DELETE ON ventaProductos
FOR EACH ROW
BEGIN
    INSERT INTO BitacoraVentas (idUsuario, idVenta, idInventario, cantidadProducto, precioVenta, montoTotal)
    VALUES (@current_user_id, OLD.idVenta, OLD.idInventario, OLD.cantidad, OLD.precioVenta, OLD.subtotal);
END //

DELIMITER ;
