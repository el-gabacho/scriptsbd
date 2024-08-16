-- AUTORES
-- Emanuel Pacheco Alberto
-- Leonel Federico Valencia Estudillo

-- ELIMINAR BASE DE DATOS

-- DROP DATABASE el_gabacho;

-- CREACION DE LA BASE DE DATOS

CREATE OR REPLACE DATABASE el_gabacho;

-- USAR LA BASE DE DATOS

USE el_gabacho;

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
	nombre VARCHAR(30) NOT NULL
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

-- procedimiento almacenado que inserta un nuevo producto en la tabla inventario, registra la relación en proveedorProductos, y también en registroProductos,
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
    -- Inicializar el parámetro de salida
    SET p_idInventario = NULL;

    -- Verificar si el código de barras ya existe
    IF EXISTS (SELECT 1 FROM inventario WHERE codigoBarras = p_codigoBarras) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Código de barras ya existe.';
    ELSE
        -- Insertar el nuevo producto
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

-- Procedimiento para insertar imagenes a un nuevo producto
DELIMITER $$

CREATE PROCEDURE proc_inserta_img_producto(
    IN p_idInventario INT,
    IN p_imgRepresentativa BOOL,
    IN p_img2 BOOL,
    IN p_img3 BOOL,
    IN p_img4 BOOL,
    IN p_img5 BOOL
)
BEGIN
    -- Verificar si el producto existe
    IF NOT EXISTS (SELECT 1 FROM inventario WHERE idInventario = p_idInventario) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El producto con el ID especificado no existe.';
    ELSE
        -- Insertar imágenes relacionadas con el producto
        INSERT INTO imagenes (idInventario, imgRepresentativa, img2, img3, img4, img5)
        VALUES (p_idInventario, p_imgRepresentativa, p_img2, p_img3, p_img4, p_img5);
    END IF;
END $$

DELIMITER ;

-- Procedimiento para insertar modelos a productos
DELIMITER $$

CREATE PROCEDURE proc_insertar_modelos_producto(
    IN p_idModelo INT,
    IN p_anioInicio INT,
    IN p_anioFin INT,
    IN p_anioTodo BOOL
)
BEGIN
    DECLARE p_idAnio INT;
    DECLARE p_idModeloAnio INT;
    DECLARE p_idModeloAutoparte INT;

    -- Verificar si el modelo existe
    IF NOT EXISTS (SELECT 1 FROM modelos WHERE idModelo = p_idModelo) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El modelo con el ID especificado no existe.';
    END IF;

    -- Manejo de años
    IF p_anioTodo = FALSE THEN
        -- Buscar o insertar el rango de años
        SELECT idAnio INTO p_idAnio
        FROM anios
        WHERE anioInicio = p_anioInicio AND anioFin = p_anioFin;
        
        IF p_idAnio IS NULL THEN
            -- Insertar nuevo rango de años
            INSERT INTO anios (anioInicio, anioFin, anioTodo)
            VALUES (p_anioInicio, p_anioFin, FALSE);
            SET p_idAnio = LAST_INSERT_ID();
        END IF;
    ELSE
        -- Buscar o insertar registro para todos los años
        SELECT idAnio INTO p_idAnio
        FROM anios
        WHERE anioTodo = TRUE;
        
        IF p_idAnio IS NULL THEN
            -- Insertar nuevo registro para todos los años
            INSERT INTO anios (anioInicio, anioFin, anioTodo)
            VALUES (0, 0, TRUE);
            SET p_idAnio = LAST_INSERT_ID();
        END IF;
    END IF;

    -- Buscar o insertar la relación modelo-año
    SELECT idModeloAnio INTO p_idModeloAnio
    FROM modeloAnios
    WHERE idModelo = p_idModelo AND idAnio = p_idAnio;
    
    IF p_idModeloAnio IS NULL THEN
        -- Insertar nueva relación modelo-año
        INSERT INTO modeloAnios (idModelo, idAnio)
        VALUES (p_idModelo, p_idAnio);
        SET p_idModeloAnio = LAST_INSERT_ID();
    END IF;

    -- Verificar si la relación modelo-año e inventario existe en modeloAutopartes
    SELECT idModeloAutoparte INTO p_idModeloAutoparte
    FROM modeloAutopartes
    WHERE idModeloAnio = p_idModeloAnio AND idInventario = p_idInventario;
    
    IF p_idModeloAutoparte IS NULL THEN
        -- Insertar nueva relación modelo-año e inventario
        INSERT INTO modeloAutopartes (idModeloAnio, idInventario)
        VALUES (p_idModeloAnio, p_idInventario);
        SET p_idModeloAutoparte = LAST_INSERT_ID();
    END IF;

END $$

DELIMITER ;


-- Editar un producto
DELIMITER $$

CREATE PROCEDURE proc_actualizar_producto(
    IN p_idInventario INT,
    IN p_idCategoria INT,
    IN p_idUnidadMedida INT,
    IN p_nombre VARCHAR(100),
    IN p_descripcion VARCHAR(150),
    IN p_cantidadActual FLOAT,
    IN p_cantidadMinima FLOAT,
    IN p_precioCompra FLOAT,
    IN p_mayoreo FLOAT,
    IN p_menudeo FLOAT,
    IN p_colocado FLOAT
)
BEGIN
    -- Verificar si el producto existe
    IF NOT EXISTS (SELECT 1 FROM inventario WHERE idInventario = p_idInventario) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El producto con el ID especificado no existe.';
    ELSE
        -- Actualizar el producto
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
END $$

DELIMITER ;

-- Ediar un producto en imagenes
DELIMITER $$

CREATE PROCEDURE proc_actualizar_imagenes_producto(
    IN p_idInventario INT,
    IN p_imgRepresentativa BOOL,
    IN p_img2 BOOL,
    IN p_img3 BOOL,
    IN p_img4 BOOL,
    IN p_img5 BOOL
)
BEGIN
    -- Verificar si el producto existe
    IF NOT EXISTS (SELECT 1 FROM inventario WHERE idInventario = p_idInventario) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El producto con el ID especificado no existe.';
    ELSE
        -- Actualizar las imágenes del producto
        INSERT INTO imagenes (idInventario, imgRepresentativa, img2, img3, img4, img5)
        VALUES (p_idInventario, p_imgRepresentativa, p_img2, p_img3, p_img4, p_img5)
        ON DUPLICATE KEY UPDATE
            imgRepresentativa = p_imgRepresentativa,
            img2 = p_img2,
            img3 = p_img3,
            img4 = p_img4,
            img5 = p_img5;
    END IF;
END $$

DELIMITER ;

-- Elimina relacion modeloautoparte 
DELIMITER $$

CREATE PROCEDURE proc_eliminar_modelo_autoparte(
    IN p_idModeloAnio INT,
    IN p_idInventario INT
)
BEGIN
    -- Verificar si la relación existe
    IF NOT EXISTS (SELECT 1 FROM modeloAutopartes WHERE idModeloAnio = p_idModeloAnio AND idInventario = p_idInventario) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La relación especificada no existe en modeloAutopartes.';
    ELSE
        -- Eliminar la relación en modeloAutopartes
        DELETE FROM modeloAutopartes
        WHERE idModeloAnio = p_idModeloAnio AND idInventario = p_idInventario;
    END IF;
END $$

DELIMITER ;

-- Este procedimiento asegurará que un producto solo se elimine físicamente si no tiene ninguna relación en ventaProductos, 
-- mientras que en caso contrario, simplemente se deshabilitará (estado = FALSE) y se registrará la acción en registroProductos.
DELIMITER //

CREATE PROCEDURE proc_eliminar_producto (
    IN p_idInventario INT,
    IN p_idUsuario INT
)
BEGIN
    DECLARE v_count INT;

    -- Verificar si el producto tiene relaciones en ventaProductos
    SELECT COUNT(*)
    INTO v_count
    FROM ventaProductos
    WHERE idInventario = p_idInventario;

    -- Si no hay relaciones en ventaProductos, permitir la eliminación
    IF v_count = 0 THEN
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


-- procedimiento almacenado que actualice el estado de un producto a FALSE en la tabla inventario 
-- y actualice el idUsuarioElimino y fechaElimino en la tabla registroProductos


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
