-- AUTORES
-- Emanuel Pacheco Alberto
-- Leonel Federico Valencia Estudillo

-- ELIMINAR BASE DE DATOS

DROP DATABASE el_gabacho;

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

-- CREACION DE LA TABLA CONFIG

CREATE TABLE config (
  correo VARCHAR(50),
  direccion VARCHAR(100),
  encabezado VARCHAR(255),
  footer VARCHAR(255),
  rfc VARCHAR(50)
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
  contrasenia VARCHAR(100) NOT NULL,
  fechaCreacion TIMESTAMP default CURRENT_TIMESTAMP,
  estado BOOL DEFAULT TRUE,
  FOREIGN KEY (idRol) REFERENCES roles(idRol)
);

-- CREACION DE LA TABLA PROVEEDORES *

CREATE TABLE proveedores (
  idProveedor INT AUTO_INCREMENT PRIMARY KEY,
  empresa VARCHAR(50) NOT NULL,
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

-- CREACION DE LA TABLA RELACION MODELO AUTOPARTES "RELACION TABLA MODELO AÑO Y INVENTARIO AUTOPARTE"

CREATE TABLE modeloAutopartes (
	idModeloAutoparte INT AUTO_INCREMENT PRIMARY KEY,
	idModeloAnio INT NOT NULL,
	idInventario INT NOT NULL,
	FOREIGN KEY (idModeloAnio) REFERENCES modeloanios(idModeloAnio) ON DELETE CASCADE,
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

-- TIGGERS PARA LA BASE DE DATOS

-- ESTE PROCEDIMIENTO HACE LO SIGUIENTE: TABLA MODELO, ANIO Y ANIOMODELO

-- VERIFICA LO QUE VAS A INSERTAR (idModelo, anioInicio, anioFin, anioTodo)
-- modelo del vehiculo ID, rango año modelo por default 0 Inicio y Fin, TRUE para todos y FALSE si existe año o rango de años

-- Primero verifica si el año insertado existe en la tabla anios:
-- 1. Si existe obtiene el ID (manda mensaje)
-- 2. Si no existe lo crea y obtiene el ID (manda mensaje)

-- Despues verifica si existe una relacion en la tabla anioModelos con el ID Modelo insertado y el ID del Año Obtenido
-- 1. Si existe, no crea nada y manda mensaje
-- 2. Si no existe, crea una nueva relacion en la tabla

DELIMITER //

CREATE OR REPLACE PROCEDURE proc_modelo_anio(
    IN proc_id_modelo INT,
    IN proc_anio_inicio INT,
    IN proc_anio_fin INT,
    IN proc_anio_todo BOOL
)
BEGIN
    DECLARE idAnio_select INT DEFAULT NULL;
    DECLARE idAnio_existe BOOLEAN DEFAULT FALSE;
    
    DECLARE idModelo_select INT DEFAULT NULL;
    DECLARE idModelo_existe BOOLEAN DEFAULT FALSE;
    
    DECLARE idModeloAnio_select INT DEFAULT NULL;

    -- Verificar si hay un año existente en la tabla Anios
    IF proc_anio_todo THEN
        -- Verificar si ya existe un registro con todo_anio verdadero
        SELECT idAnio INTO idAnio_select
        FROM anios
        WHERE anioInicio = 0 AND anioFin = 0 AND anioTodo = TRUE
        LIMIT 1;
    ELSE
        -- Verificar si ya existe un registro con las mismas fechas
        SELECT idAnio INTO idAnio_select
        FROM anios
        WHERE anioInicio = proc_anio_inicio AND anioFin = proc_anio_fin AND anioTodo = FALSE
        LIMIT 1;
    END IF;

    -- Verifica si el año es existente (si es nulo), en caso contrario lo crea
    IF idAnio_select IS NOT NULL THEN
        -- Existe el año en la tabla Anios y manda ID
        SET idAnio_existe = TRUE;
        SELECT CONCAT('Existe el año en la tabla ANIOS ID: ', idAnio_select) AS mensaje;
    ELSE
        -- Insertar el año/rango en la tabla Anios
        INSERT INTO anios (anioInicio, anioFin, anioTodo)
        VALUES (proc_anio_inicio, proc_anio_fin, proc_anio_todo);

        -- Obtener el idAnio recién insertado y manda ID
        SET idAnio_select = LAST_INSERT_ID();
        
        SET idAnio_existe = FALSE;
        
        SELECT CONCAT('El año ha sido insertado correctamente en la tabla ANIOS ID: ', idAnio_select) AS mensaje;
    END IF;

    -- Verifica si el idModelo ingresado existe en la tabla Modelos
    SELECT idModelo INTO idModelo_select
    FROM modelos
    WHERE idModelo = proc_id_modelo
    LIMIT 1;
    
    -- Verifica si el modelo es existente (si es nulo), en caso contrario lo crea
    IF idModelo_select IS NOT NULL THEN
        -- Existe el modelo en la tabla Modelos y manda ID
        SET idModelo_existe = TRUE;
        SELECT CONCAT('Existe el modelo en la tabla MODELOS ID: ', idModelo_select) AS mensaje;
    ELSE
        -- No existe el modelo
        SET idModelo_existe = FALSE;
        SELECT CONCAT('El modelo no existe en la tabla modelo, IMPOSIBLE HACER UNA RELACION ') AS mensaje;
    END IF;

    -- Verifica si el modelo con el año es existente manda mensaje de exito, en caso contrario creala
    IF idModelo_existe = FALSE THEN 
        SELECT 'IMPOSIBLE RELACIONAR EL MODELO CON UN AÑO, POR QUE NO EXISTE EL MODELO. VERIFICA' AS mensaje2;
    ELSE
        -- Verificar si ya existe un registro en la tabla MODELOANIOS
        SELECT idModeloAnio INTO idModeloAnio_select
        FROM modeloanios
        WHERE idModelo = idModelo_select AND idAnio = idAnio_select
        LIMIT 1;
        
        -- Si la relación existe, mostrar mensaje
        IF idModeloAnio_select IS NOT NULL THEN
            SELECT CONCAT('Existe la relación del modelo con el año en la tabla ANIO_MODELOS ID: ', idModeloAnio_select) AS mensaje2;
        ELSE
            -- Si no existe, insertar la relación
            INSERT INTO modeloAnios (idModelo, idAnio)
            VALUES (proc_id_modelo, idAnio_select);
            
            SET idModeloAnio_select = LAST_INSERT_ID();
            
            SELECT CONCAT('La relación ha sido insertada modelo con el año en la tabla ANIO_MODELOS ID: ', idModeloAnio_select) AS mensaje2;
        END IF;
    END IF;
END //

DELIMITER ;


-- ---------------------------- 
-- RELACONA LA TABLA MODELO AUTOPARTE CON EL MODELOANIO ... UTILIZADA
DELIMITER //

CREATE OR REPLACE PROCEDURE proc_modeloanio_autoparte(
    IN proc_id_inventario INT,
    IN proc_id_modeloAnio INT
)
BEGIN

    DECLARE idInventario_select INT DEFAULT NULL;
    DECLARE idInventario_existe BOOLEAN DEFAULT FALSE;
    
    DECLARE idModeloAnio_select INT DEFAULT NULL;
    DECLARE idModeloAnio_existe BOOLEAN DEFAULT FALSE;
    
    DECLARE idModeloAutoparte_select INT DEFAULT NULL;
    
    -- INVENTARIO -------------------------------------------------------------------------------------------
    -- Obtener el idInventario
    IF proc_id_inventario IS NOT NULL THEN
        SELECT idInventario INTO idInventario_select
        FROM inventario
        WHERE idInventario = proc_id_inventario;
    END IF;
    
    -- Verifica si el idInventario es existente (si no es nulo)
    IF idInventario_select IS NOT NULL THEN
        -- Existe el ID del Inventario
        SET idInventario_existe = TRUE;
        SELECT CONCAT('Existe la parte en el INVENTARIO ID: ', idInventario_select) AS mensaje;
    ELSE
        -- No existe el ID en el inventario
        SET idInventario_existe = FALSE;
        SELECT CONCAT('No existe la parte en el INVENTARIO que desea relacionar ERROR: ', proc_id_inventario) AS mensaje;
    END IF;
    
    -- MODELO ANIOS -------------------------------------------------------------------------------------------
    -- Obtener el ID de ModeloAnios
    IF proc_id_modeloAnio IS NOT NULL THEN
        SELECT idModeloAnio INTO idModeloAnio_select
        FROM modeloanios
        WHERE idModeloAnio = proc_id_modeloAnio;
    END IF;
    
    -- Verifica si el idModeloAnio existe (si no es nulo)
    IF idModeloAnio_select IS NOT NULL THEN
        -- Existe el ID del idModeloAnio
        SET idModeloAnio_existe = TRUE;
        SELECT CONCAT('Existe el MODELOANIO ID: ', idModeloAnio_select) AS mensaje;
    ELSE
        -- No existe el ID del idModeloAnio
        SET idModeloAnio_existe = FALSE;
        SELECT CONCAT('No existe el MODELOANIO que desea relacionar ID: ', proc_id_modeloAnio) AS mensaje;
    END IF;
    
    -- MODELO AUTOPARTES -------------------------------------------------------------------------------------------	 
    -- Verifica si la relación existe en la tabla MODELOAUTOPARTES
    IF idInventario_existe IS TRUE AND idModeloAnio_existe IS TRUE THEN
        -- Realiza una consulta con los mismos datos existentes, si existe un registro ya existente
        SELECT idModeloAutoparte INTO idModeloAutoparte_select
        FROM modeloAutopartes
        WHERE idModeloAnio = proc_id_modeloAnio 
          AND idInventario = proc_id_inventario;
          
        -- Verifica si idModeloAutoparte_select obtuvo un id de registro existente
        IF idModeloAutoparte_select IS NOT NULL THEN
            SELECT CONCAT('La relación entre el autoparte y el modelo ya existe en MODELOAUTOPARTE ID: ', idModeloAutoparte_select) AS mensaje;
        ELSE
            -- Insertar la relación en modeloAutopartes si no existe
            INSERT INTO modeloAutopartes (idModeloAnio, idInventario)
            VALUES (proc_id_modeloAnio, proc_id_inventario);
        
            -- Obtener el id del registro previamente insertado
            SET idModeloAutoparte_select = LAST_INSERT_ID();
            SELECT CONCAT('La relación entre el autoparte y el modelo ha sido creada exitosamente en MODELOAUTOPARTE ID: ', idModeloAutoparte_select) AS mensaje;
        END IF;
    ELSE
        SELECT 'ERROR: Verifica si el ID Inventario o ID ModeloAnios, si existen o si ambos existen.' AS mensaje;
    END IF;
END //

DELIMITER ;

-- ////////////////////////////////////////////////////////////////////////////////////////
-- procedimiento almacenado que inserta un nuevo producto en la tabla inventario, registra la relación en proveedorProductos, y también en registroProductos,
DELIMITER //

CREATE OR REPLACE PROCEDURE proc_insertar_producto (
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
    OUT p_v_idInventario INT
)
BEGIN
    DECLARE v_idInventario INT;
    DECLARE v_estado BOOL;

    -- Verificar si el codigoBarras ya existe
    SELECT idInventario, estado INTO v_idInventario, v_estado
    FROM inventario
    WHERE codigoBarras = p_codigoBarras;
	
	-- Si el codigoBarras existe, devolver un error.
    IF v_idInventario IS NOT NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El producto con el código de barras especificado no puedes utilizarlo.';
    -- Insertar un nuevo registro si el codigoBarras no existe
    ELSE
        INSERT INTO inventario (
            idCategoria, idUnidadMedida, codigoBarras, nombre, descripcion,
            cantidadActual, cantidadMinima, precioCompra, mayoreo, menudeo, colocado
        ) VALUES (
            p_idCategoria, p_idUnidadMedida, p_codigoBarras, p_nombre, p_descripcion,
            p_cantidadActual, p_cantidadMinima, p_precioCompra, p_mayoreo, p_menudeo, p_colocado
        );

        SET v_idInventario = LAST_INSERT_ID();
        	
			-- Registrar en proveedorProductos
    		INSERT INTO proveedorProductos (idProveedor, idInventario)
    		VALUES (p_idProveedor, v_idInventario);

    		-- Registrar en registroProductos
    		INSERT INTO registroProductos (idInventario, idUsuarioRegistro)
    		VALUES (v_idInventario, p_idUsuario);
    END IF;
    -- Asignar el id del inventario al parámetro de salida
    SET p_v_idInventario = v_idInventario;
END //

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
    
    -- Actualizar el estado del pagoVenta a FALSE
    DELETE FROM pagoVenta
    WHERE idVenta = p_idVenta;

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
	SELECT idInventario INTO p_idInventario FROM ventaProductos WHERE idVentaProducto = p_idVentaProducto; 
	SELECT cantidad INTO p_cantidadDevuelta FROM ventaProductos WHERE idVentaProducto = p_idVentaProducto; 
	
    -- Eliminar producto en ventaProductos
    DELETE FROM ventaProductos
    WHERE idVenta = p_idVenta AND idVentaProducto = p_idVentaProducto;

    -- Actualizar la cantidad en el inventario
    UPDATE inventario
    SET cantidadActual = cantidadActual + p_cantidadDevuelta,
    		estado = TRUE
    WHERE idInventario = p_idInventario;

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
        v_existenciasActualizado = v_existenciasActual - (p_cantidad - v_cantidadOriginal);
    ELSE
        v_existenciasActualizado = v_existenciasActual + (v_cantidadOriginal - p_cantidad);
    END IF;

    -- Actualizar la cantidad en ventaProductos
    UPDATE ventaProductos
    SET cantidad = p_cantidad, 
        tipoVenta = p_tipoVenta
    	precioVenta = p_precioActualizado,
        subtotal = cantidad * precioVenta
    WHERE idVenta = p_idVenta AND idVentaProducto = p_idVentaProducto;
    -- Si toda la cantidad del producto ha sido devuelta, cambiar su estado a FALSE
    IF p_cantidadDevuelta = v_cantidadOriginal THEN
        DELETE FROM ventaProductos
    	  WHERE idVenta = p_idVenta AND idVentaProducto = p_idVentaProducto;
    END IF;

    -- Actualizar la cantidad en el inventario
    UPDATE inventario
    SET cantidadActual = v_existenciasActualizado
    WHERE idInventario = p_idInventario;

    -- Actualizar el montoTotal de la venta
    UPDATE ventas v
    JOIN (
        SELECT idVenta, SUM(subtotal) AS nuevoMontoTotal
        FROM ventaProductos
        WHERE idVenta = p_idVenta AND estado = TRUE
        GROUP BY idVenta
    ) vp ON v.idVenta = vp.idVenta
    SET v.montoTotal = vp.nuevoMontoTotal
    WHERE v.idVenta = p_idVenta;
    
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
