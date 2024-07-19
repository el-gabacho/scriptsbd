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
    IN p_urlImagen VARCHAR(300),
    IN p_idProveedor INT,
    IN p_idUsuario INT
)
BEGIN
    DECLARE v_idInventario INT;

    -- Verificar si el codigoBarras ya existe y tiene estado FALSE
    SELECT idInventario INTO v_idInventario
    FROM inventario
    WHERE codigoBarras = p_codigoBarras AND estado = FALSE;

    -- Si el codigoBarras existe y tiene estado FALSE, actualizar el registro
    IF v_idInventario IS NOT NULL THEN
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
            colocado = p_colocado,
            urlImagen = p_urlImagen,
            estado = TRUE
        WHERE idInventario = v_idInventario;
			
			UPDATE registroProductos
			SET idUsuarioRegistro = p_idUsuario,
				fechaCreacion = NOW()
			WHERE idInventario = v_idInventario;
    -- Insertar un nuevo registro si el codigoBarras no existe
    ELSE
        INSERT INTO inventario (
            idCategoria, idUnidadMedida, codigoBarras, nombre, descripcion,
            cantidadActual, cantidadMinima, precioCompra, mayoreo, menudeo, colocado, urlImagen
        ) VALUES (
            p_idCategoria, p_idUnidadMedida, p_codigoBarras, p_nombre, p_descripcion,
            p_cantidadActual, p_cantidadMinima, p_precioCompra, p_mayoreo, p_menudeo, p_colocado, p_urlImagen
        );

        SET v_idInventario = LAST_INSERT_ID();
        	
			-- Registrar en proveedorProductos
    		INSERT INTO proveedorProductos (idProveedor, idInventario)
    		VALUES (p_idProveedor, v_idInventario);

    		-- Registrar en registroProductos
    		INSERT INTO registroProductos (idInventario, idUsuarioRegistro)
    		VALUES (v_idInventario, p_idUsuario);
    END IF;

    
END //

DELIMITER ;

-- Trigger para actualizar registroProductos despues de eliminar un producto del inventario
DELIMITER //

CREATE TRIGGER trigg_after_inventario_delete
AFTER DELETE ON inventario
FOR EACH ROW
BEGIN
    UPDATE registroProductos
    SET idUsuarioElimino = @current_user_id,
        fechaElimino = NOW()
    WHERE idInventario = OLD.idInventario;
END //

DELIMITER ;

-- rocedimiento para eliminar un producto
DELIMITER //

CREATE PROCEDURE proc_eliminar_producto (
    IN p_idInventario INT,
    IN p_idUsuario INT
)
BEGIN
    -- Configurar la variable de sesión con el id del usuario
    SET @current_user_id = p_idUsuario;
    
    -- Eliminar el producto de la tabla inventario
    DELETE FROM inventario
    WHERE idInventario = p_idInventario;
END //

DELIMITER ;

-- procedimiento almacenado que actualice el estado de un producto a FALSE en la tabla inventario 
-- y actualice el idUsuarioElimino y fechaElimino en la tabla registroProductos


-- ventas Paso 1: Crear una Venta
DELIMITER //

CREATE PROCEDURE proc_crear_venta (
    IN p_idUsuario INT,
    IN p_idCliente INT
)
BEGIN
    INSERT INTO ventas (idUsuario, idCliente, montoTotal, recibioDinero, folioTicket, imprimioTicket)
    VALUES (p_idUsuario, p_idCliente, 0, 0, '', FALSE);
END //

DELIMITER ;

-- ventas Paso 2: Agregar Producto a la Venta
DELIMITER //

CREATE OR REPLACE PROCEDURE proc_agregar_producto_venta (
    IN p_idVenta INT,
    IN p_idInventario INT,
    IN p_cantidad FLOAT,
    IN p_tipoVenta VARCHAR(50),
    IN p_precioVenta FLOAT
)
BEGIN
    DECLARE v_subtotal FLOAT;
    
    SET v_subtotal = p_cantidad * p_precioVenta;

    INSERT INTO ventaProductos (idVenta, idInventario, cantidad, tipoVenta, precioVenta, subtotal)
    VALUES (p_idVenta, p_idInventario, p_cantidad, p_tipoVenta, p_precioVenta, v_subtotal);
    
    -- Actualizar la catidad de cada producto
    UPDATE inventario
    SET cantidadActual = cantidadActual - p_cantidad
    WHERE idInventario = p_idInventario;
END //
	
DELIMITER ;

-- ventas Paso 3: Finalizar la Venta
DELIMITER //

CREATE PROCEDURE proc_finalizar_venta (
    IN p_idVenta INT,
    IN p_recibioDinero FLOAT,
    IN p_folioTicket VARCHAR(50),
    IN p_imprimioTicket BOOL,
    IN p_idTipoPago INT,
    IN p_referenciaUnica VARCHAR(50),
    IN p_descripcion VARCHAR(50)
)
BEGIN
    DECLARE v_montoTotal FLOAT;

    -- Calcular el monto total sumando los subtotales de los productos en la venta
    SELECT SUM(subtotal) INTO v_montoTotal
    FROM ventaProductos
    WHERE idVenta = p_idVenta AND estado = TRUE;

    -- Actualizar el registro de la venta con el monto total y otros detalles
    UPDATE ventas
    SET montoTotal = v_montoTotal,
        recibioDinero = p_recibioDinero,
        folioTicket = p_folioTicket,
        imprimioTicket = p_imprimioTicket
    WHERE idVenta = p_idVenta;

    -- Registrar el pago en la tabla pagoVenta
    INSERT INTO pagoVenta (idVenta, idTipoPago, referenciaUnica, descripcion)
    VALUES (p_idVenta, p_idTipoPago, p_referenciaUnica, p_descripcion);
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
        DELETE ventaProductos
        WHERE idVenta = p_idVenta AND idInventario = v_idInventario;
    END LOOP;
    
     -- Cerrar el cursor
    CLOSE cur;
    
    -- Actualizar el estado del pagoVenta a FALSE
    DELETE pagoVenta
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
    DELETE ventaProductos
    WHERE idVenta = p_idVenta AND idVentaProducto = p_idVentaProducto;

    -- Actualizar la cantidad en el inventario
    UPDATE inventario
    SET cantidadActual = cantidadActual + p_cantidadDevuelta
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
    IN p_cantidadDevuelta FLOAT,
    IN p_precioActualizado FLOAT
)
BEGIN
	DECLARE p_idInventario INT;
	DECLARE v_cantidadOriginal FLOAT;
	
	SELECT idInventario INTO p_idInventario FROM ventaProductos WHERE idVentaProducto = p_idVentaProducto; 
	
    -- Obtener la cantidad original del producto en la venta
    SELECT cantidad INTO v_cantidadOriginal
    FROM ventaProductos
    WHERE idVenta = p_idVenta AND idVentaProducto = p_idVentaProducto;

    -- Validar que la cantidad devuelta no sea mayor que la cantidad original
    IF p_cantidadDevuelta > v_cantidadOriginal THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cantidad devuelta no puede ser mayor que la cantidad vendida';
    END IF;

    -- Actualizar la cantidad en ventaProductos
    UPDATE ventaProductos
    SET cantidad = cantidad - p_cantidadDevuelta, 
    	  precioVenta = p_precioActualizado,
        subtotal = cantidad * precioVenta
    WHERE idVenta = p_idVenta AND idVentaProducto = p_idVentaProducto;

    -- Si toda la cantidad del producto ha sido devuelta, cambiar su estado a FALSE
    IF p_cantidadDevuelta = v_cantidadOriginal THEN
        DELETE ventaProductos
    	  WHERE idVenta = p_idVenta AND idVentaProducto = p_idVentaProducto;
    END IF;

    -- Actualizar la cantidad en el inventario
    UPDATE inventario
    SET cantidadActual = cantidadActual + p_cantidadDevuelta
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