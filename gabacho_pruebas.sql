-- ELIMINAR BASE DE DATOS

DROP DATABASE el_gabacho_prueba;

-- CREACION DE LA BASE DE DATOS

CREATE OR REPLACE DATABASE el_gabacho_prueba;

-- USAR LA BASE DE DATOS

 USE el_gabacho_prueba;
 
 -- CREACION DE LA TABLA MARCAS

CREATE TABLE marcas (
    idMarca INT AUTO_INCREMENT PRIMARY KEY,
    nombreMarca VARCHAR(40) NOT NULL UNIQUE,
    urlLogo VARCHAR(300),
    estado BOOL DEFAULT TRUE
    -- UNIQUE INDEX unique_nombreMarca (nombreMarca)
);

-- CREACION DE LA TABLA MODELOS

CREATE TABLE modelos (
    idModelo INT AUTO_INCREMENT PRIMARY KEY,
    idMarca INT NOT NULL,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    estado BOOL DEFAULT TRUE,
    FOREIGN KEY (idMarca) REFERENCES marcas(idMarca) ON DELETE CASCADE
    -- INDEX idx_nombre (nombre)
);


-- CREACION DE LA TABLA AÑO MODELOS

CREATE TABLE anioModelos (
    idAnioModelo INT AUTO_INCREMENT PRIMARY KEY,
    anioModeloInicio INT UNSIGNED NOT NULL DEFAULT 0,
    anioModeloFin INT UNSIGNED NOT NULL DEFAULT 0,
    todoAnio BOOL DEFAULT FALSE,
    UNIQUE (anioModeloInicio, anioModeloFin)
    -- INDEX idx_anioModeloInicio (anioModeloInicio),
    -- INDEX idx_anioModeloFin (anioModeloFin),
    -- INDEX idx_todoAnio (todoAnio)
);


-- CREACION DE LA TABLA RELACION MODELO AÑOS "RELACION TABLA MODELOS Y AÑO MODELOS"

CREATE TABLE modeloAnios (
    idModeloAnio INT AUTO_INCREMENT PRIMARY KEY,
    idModelo INT NOT NULL,
    idAnioModelo INT NOT NULL,
    estado BOOL DEFAULT TRUE,
    FOREIGN KEY (idModelo) REFERENCES modelos(idModelo) ON DELETE CASCADE,
    FOREIGN KEY (idAnioModelo) REFERENCES anioModelos(idAnioModelo)
    -- INDEX idx_idModelo (idModelo),
    -- INDEX idx_idAnioModelo (idAnioModelo)
);

-- CREACION DE LA TABLA INVENTARIO AUTOPARTES

CREATE TABLE inventarioAutoparte (
    idInventario INT AUTO_INCREMENT PRIMARY KEY,
    idCategoria INT,
    idUnidadMedida INT NOT NULL,
    codigoBarras VARCHAR(50) NOT NULL UNIQUE,
    nombreParte VARCHAR(100) NOT NULL,
    descripcionParte VARCHAR(150) NOT NULL,
    cantidadActual FLOAT UNSIGNED DEFAULT 0 NOT NULL,
    cantidadMinima FLOAT UNSIGNED DEFAULT 1 NOT NULL,
    precioCompra FLOAT UNSIGNED DEFAULT 0.00 NOT NULL,
    mayoreo FLOAT UNSIGNED DEFAULT 0.00 NOT NULL,
    menudeo FLOAT UNSIGNED DEFAULT 0.00 NOT NULL,
    colocado FLOAT UNSIGNED DEFAULT 0.00 NOT NULL,
    urlImagen VARCHAR(300),
    estado BOOL DEFAULT TRUE,
    FOREIGN KEY (idCategoria) REFERENCES categorias(idCategoria),
    FOREIGN KEY (idUnidadMedida) REFERENCES unidadMedidas(idUnidadMedida)
    -- INDEX idx_codigoBarras (codigoBarras)
);

-- CREACION DE LA TABLA RELACION MODELO AUTOPARTES "RELACION TABLA MODELO AÑO Y INVENTARIO AUTOPARTE"

CREATE TABLE modeloAutopartes (
    idModeloAutoparte INT AUTO_INCREMENT PRIMARY KEY,
    idModeloAnio INT NOT NULL,
    idInventario INT NOT NULL,
    estado BOOL DEFAULT TRUE,
    FOREIGN KEY (idModeloAnio) REFERENCES modeloAnios(idModeloAnio) ON DELETE CASCADE
    -- INDEX idx_idModeloAnio (idModeloAnio),
    -- INDEX idx_idInventario (idInventario)
);

  -- CREACION DE LA TABLA CATEGORIAS

CREATE TABLE categorias (
  idCategoria INT AUTO_INCREMENT PRIMARY KEY,
  nombreCategoria VARCHAR(50) NOT NULL
);

-- CREACION DE LA TABLA UNIDAD MEDIDAS ** OCULTO ** = M/CM ó PQ/PZ

CREATE TABLE unidadMedidas (
  idUnidadMedida INT AUTO_INCREMENT PRIMARY KEY,
  tipoMedida VARCHAR(8) NOT NULL,
  descripcionMedida VARCHAR(100)
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
  contrasenia VARCHAR(15) NOT NULL,
  fechaCreacion TIMESTAMP default CURRENT_TIMESTAMP,
  estado BOOL DEFAULT TRUE,
  FOREIGN KEY (idRol) REFERENCES roles(idRol)
);

-- CREACION DE LA TABLA PROVEEDORES

CREATE TABLE proveedores (
  idProveedor INT AUTO_INCREMENT PRIMARY KEY,
  empresa VARCHAR(50) NOT NULL,
  nombreEncargado VARCHAR(50),
  telefono VARCHAR(10),
  correo VARCHAR(50)
);

-- CREACION DE LA TABLA RELACION PROVEEDOR PRODUCTOS "RELACION TABLA PROVEEDORES Y INVENTARIO AUTOPARTES"

CREATE TABLE proveedorProductos (
  idProveedorProducto INT AUTO_INCREMENT PRIMARY KEY,
  idProveedor INT NOT NULL,
  idInventario INT NOT NULL,
  FOREIGN KEY (idProveedor) REFERENCES proveedores(idProveedor)
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
  FOREIGN KEY (idInventario) REFERENCES inventarioAutoparte(idInventario)
);

-- CREACION DE LA TABLA RELACION REGISTRO PRODUCTOS "RELACION TABLA USUARIOS Y INVENTARIO AUTOPARTES"

CREATE TABLE registroProductos (
  idRegistroProducto INT AUTO_INCREMENT PRIMARY KEY,
  idInventario INT NOT NULL,
  idUsuarioRegistro INT NOT NULL,
  fechaCreacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  idUsuarioElimino INT DEFAULT NULL,
  fechaElimino TIMESTAMP DEFAULT NULL,
  FOREIGN KEY (idInventario) REFERENCES inventarioAutoparte(idInventario),
  FOREIGN KEY (idUsuarioRegistro) REFERENCES usuarios(idUsuario)
  );
  
  -- CREACION DE LA TABLA CLIENTES = PUBLICO GENERAL

CREATE TABLE clientes (
	idCliente INT AUTO_INCREMENT PRIMARY KEY,
	nombreCliente VARCHAR(30) NOT NULL
);

-- CREACION DE LA TABLA TIPO PAGOS ** OCULTO ** = EFECTIVO, CARJETA, TRANSFERENCIA, DEPOSITO

CREATE TABLE tipoPagos (
	idTipoPago INT AUTO_INCREMENT PRIMARY KEY,
   tipoPago VARCHAR(20) NOT NULL,
   descripcion VARCHAR(100)
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
  estado BOOL DEFAULT TRUE,
  FOREIGN KEY (idUsuario) REFERENCES usuarios(idUsuario),
  FOREIGN KEY (idCliente) REFERENCES clientes(idCliente)
);

-- CREACION DE LA TABLA RELACION PAGO VENTAS "RELACION TABLA VENTAS Y TIPO PAGOS"

CREATE TABLE pagoVenta (
  idPagoVenta INT AUTO_INCREMENT PRIMARY KEY,
  idVenta INT NOT NULL,
  idTipoPago INT NOT NULL,
  referenciaUnica VARCHAR(50),
  descripcionPago VARCHAR(50),
  estado BOOL DEFAULT TRUE,
  FOREIGN KEY (idVenta) REFERENCES ventas(idVenta),
  FOREIGN KEY (idTipoPago) REFERENCES tipoPagos(idTipoPago)
);

-- CREACION DE LA TABLA RELACION VENTA PRODUCTOS "RELACION TABLA INVENTARIO AUTOPARTES Y VENTAS"

CREATE TABLE ventaProductos (
  idVentaProductos INT AUTO_INCREMENT PRIMARY KEY,
  idVenta INT NOT NULL,
  idInventario INT NOT NULL,
  cantidad FLOAT UNSIGNED NOT NULL,
  tipoVenta VARCHAR(50) NOT NULL,
  precioVenta FLOAT UNSIGNED NOT NULL,
  subtotal FLOAT UNSIGNED NOT NULL,
  estado BOOL DEFAULT TRUE,
  FOREIGN KEY (idVenta) REFERENCES ventas(idVenta),
  FOREIGN KEY (idInventario) REFERENCES inventarioAutoparte(idInventario)
);

-- ----------------------------------------------------------------------------------------------------------------------------

-- INSERTAR MARCAS (nombreMarca y LogoURL)
INSERT INTO marcas (nombreMarca, urlLogo) VALUES
('ACURA','https://lofrev.net/wp-content/photos/2014/08/Acura-logo.gif'),
('ALFA ROMEO', NULL),
('AMC', NULL);

-- Inserts para la tabla modelos (idModelo y nombre del modelo)
INSERT INTO modelos (idMarca, nombre) VALUES (1, 'CL');
INSERT INTO modelos (idMarca, nombre) VALUES (1, 'CSX');
INSERT INTO modelos (idMarca, nombre) VALUES (2, '1500');

-- INSERCIONES A LA TABLA UNIDAD MEDIDAS (SOLO 2 TIPOS)

INSERT INTO unidadmedidas (tipoMedida, descripcionMedida) VALUES ("PQ / PZ","Conteo por unidad");
INSERT INTO unidadmedidas (tipoMedida, descripcionMedida) VALUES ("M / CM","Usa enteros y 2 decimales para agranel");


-- INSERCIONES A LA TABLA ROLES (SOLO 3 ROLES)

INSERT INTO roles (nombre, descripcion) VALUES ("ADMINISTRADOR","Usuario que tendra todos los privilegios");
INSERT INTO roles (nombre, descripcion) VALUES ("ALMACEN","Encargado y acceso a ciertas vistas que el admin");
INSERT INTO roles (nombre, descripcion) VALUES ("CAJERO","Solo es atender y realizar una venta");

-- INSERCIONES A LA TABLA USUARIOS CON LOS ROLES

INSERT INTO usuarios (idRol, nombreCompleto, usuario, contrasenia) VALUES (1, "Juan", "Juan123", "Juan123@");
INSERT INTO usuarios (idRol, nombreCompleto, usuario, contrasenia) VALUES (2, "Francisco", "Francisco123", "Francisco123@");
INSERT INTO usuarios (idRol, nombreCompleto, usuario, contrasenia) VALUES (3, "Alma", "Alma123", "Alma123@");

-- INSERCIONES A LA TABLA PROVEEDORES
INSERT INTO proveedores (empresa) VALUES
('CITSA'),
('EUROGLAS');

-- INSERCIONES A LA TABLA CATEGORIAS

INSERT INTO categorias (nombreCategoria) VALUES ('ABRAZADERAS SUSPENSION');
INSERT INTO categorias (nombreCategoria) VALUES ('AJUSTADORES DE SUSPENSION');
INSERT INTO categorias (nombreCategoria) VALUES ('AJUSTE DE UNIDAD');

-- INSERCIONES A LA TABLA CLIENTES
INSERT INTO clientes (nombreCliente) VALUES ('PUBLICO GENERAL');

-- INSERCIONES A LA TABLA TIPO PAGO (SOLO 4 TIPOS)

INSERT INTO tipopagos (tipoPago, descripcion) VALUES ("EFECTIVO","Pago hecho en el local");
INSERT INTO tipopagos (tipoPago, descripcion) VALUES ("TARJETA","Pago hecho en el local");
INSERT INTO tipopagos (tipoPago, descripcion) VALUES ("TRANSFERENCIA","Recibe foto de la tranferencia hecha");
INSERT INTO tipopagos (tipoPago, descripcion) VALUES ("DEPOSITO","Recibe foto del ticket del deposito hecha");

-- Relacionar modelo con un año
-- Parametros (idModelo, anioInicio, anioFin, todoAnio )
CALL InsertarModeloConAnio(1, 2022, 2024, FALSE);
CALL InsertarModeloConAnio(2, 2022, 2024, FALSE);

SELECT * FROM marcas;

SELECT * FROM modelos;

SELECT * FROM aniomodelos;

SELECT * FROM modeloanios;

SELECT * FROM modelos WHERE idModelo = 1;


-- modelos con su marca

SELECT marcas.nombreMarca AS MARCA, modelos.nombre AS MODELO 
FROM marcas, modelos
WHERE marcas.idMarca = modelos.idMarca;

-- Eliminacion directa 

DELETE FROM marcas WHERE idMarca = 1;

-- RESETEAR, ELIMINA FILAS Y EMPIEZA DESDE UNO
DELETE FROM marcas;
ALTER TABLE marcas AUTO_INCREMENT = 1;

DELETE FROM modelos;
ALTER TABLE modelos AUTO_INCREMENT = 1;

DELETE FROM aniomodelos;
ALTER TABLE aniomodelos AUTO_INCREMENT = 1;

DELETE FROM modeloanios;
ALTER TABLE modeloanios AUTO_INCREMENT = 1;

-- 
CALL InsertarModeloConAnio(1, 2020, 0, FALSE);
CALL InsertarModeloConAnio(modelo_id, anio_inicio, anio_fin, todo_anio)

-- ----------------------------------------------------------------------------------------------------------------------------------------------

-- CONSULTA ELIMINA CASCADA

SELECT marcas.idMarca AS ID_MARCA, marcas.nombreMarca AS Marca,
modelos.idModelo AS ID_MODELO, modelos.nombre AS Modelo,
aniomodelos.idAnioModelo AS ID_AÑO, aniomodelos.anioModeloInicio AS INICIO, aniomodelos.anioModeloFin AS FIN,
modeloanios.idModeloAnio AS ID_RELACION_MODELO_AÑOS
FROM marcas, modelos, aniomodelos, modeloanios
WHERE marcas.idMarca = modelos.idMarca AND 
modelos.idModelo = modeloanios.idModelo AND
aniomodelos.idAnioModelo = modeloanios.idAnioModelo;

UPDATE marcas SET estado = 0 WHERE nombreMarca = 'ACURA';

CALL InsertarModeloConAnio(1, 2020, 0, FALSE);

SELECT * FROM modelos;

SELECT marcas.nombreMarca AS Marca, marcas.estado AS EstadoMarca,
modelos.nombre AS Modelo, modelos.estado AS EstadoModelo,
modeloanios.estado AS ModeloAniosEstado,
aniomodelos.anioModeloInicio AS Año_Inicio, aniomodelos.anioModeloFin AS Año_Fin
FROM marcas, modelos, aniomodelos, modeloanios
WHERE marcas.nombreMarca = 'ACURA' AND 
modelos.idModelo = modeloanios.idModelo AND
aniomodelos.idAnioModelo = modeloanios.idAnioModelo;
-- ----------------------------------------------------------------------------------------------------------------------------------------------

-- ******************************************
-- SIRVE PARA ELIMINAR EN CASCADA UNA MARCA

DROP TRIGGER marca_elimina_cascada;

DELIMITER //

CREATE TRIGGER marca_elimina_cascada
AFTER UPDATE ON marcas
FOR EACH ROW
BEGIN
    IF NEW.estado = 0 AND OLD.estado <> 0 THEN
        -- Actualizar modelos
        UPDATE modelos
        SET estado = 0
        WHERE idMarca = NEW.idMarca;

        -- Actualizar modeloAnios
        UPDATE modeloAnios
        INNER JOIN modelos ON modeloAnios.idModelo = modelos.idModelo
        SET modeloAnios.estado = 0
        WHERE modelos.idMarca = NEW.idMarca;

        -- Actualizar modeloAutopartes
        UPDATE modeloAutopartes
        INNER JOIN modeloAnios ON modeloAutopartes.idModeloAnio = modeloAnios.idModeloAnio
        INNER JOIN modelos ON modeloAnios.idModelo = modelos.idModelo
        SET modeloAutopartes.estado = 0
        WHERE modelos.idMarca = NEW.idMarca;
    END IF;
END //

DELIMITER ;

-- ************************************************************************

-- TRIGGER: ANTES DE INSERTAR UN MARCA, VALIDA SI EXISTE EL NOMBRE DE ESA MARCA.
-- CONDICIONES:
-- SI EXISTE EL NOMBRE DE LA MARCA Y NO PONE UN URL, ACTIVAR ESTATUS.
-- SI EXISTE EL NOMBRE DE LA MARCA Y INGRESA UN NUEVO URL, ACTIVAR ESTATUS Y ACTUALIZA EL CAMPO URL.
-- SI NO EXISTE EL NOMBRE DE LA MARCA Y SI INGRESA O NO INGRESA UN URL, CREALO.
DROP TRIGGER marca_actualiza_cascada;

DELIMITER //

CREATE TRIGGER marca_actualiza_cascada
AFTER UPDATE ON marcas
FOR EACH ROW
BEGIN
    IF NEW.estado = TRUE AND OLD.estado <> TRUE THEN
        -- Actualizar modelos
        UPDATE modelos
        SET estado = TRUE
        WHERE idMarca = NEW.idMarca;

        -- Actualizar modeloAnios
        UPDATE modeloAnios
        INNER JOIN modelos ON modeloAnios.idModelo = modelos.idModelo
        SET modeloAnios.estado = TRUE
        WHERE modelos.idMarca = NEW.idMarca;

        -- Actualizar modeloAutopartes
        UPDATE modeloAutopartes
        INNER JOIN modeloAnios ON modeloAutopartes.idModeloAnio = modeloAnios.idModeloAnio
        INNER JOIN modelos ON modeloAnios.idModelo = modelos.idModelo
        SET modeloAutopartes.estado = TRUE
        WHERE modelos.idMarca = NEW.idMarca;
    END IF;
END //

DELIMITER ;

-- ******************************************
-- Relaciona el modelo con el Año UTILIZADA
DROP PROCEDURE InsertarModeloConAnio;

DESCRIBE aniomodelos; -- encargada de los años

DESCRIBE modeloanios; 

DELIMITER //

CREATE OR REPLACE PROCEDURE InsertarModeloConAnio(
    IN proc_modelo_id INT,
    IN proc_anio_inicio INT,
    IN proc_anio_fin INT,
    IN proc_todo_anio BOOL
)
BEGIN

    DECLARE idRegistro INT DEFAULT NULL;
    DECLARE idRegistroMA INT DEFAULT NULL;
    DECLARE anioexiste BOOLEAN DEFAULT FALSE;

    -- Verificar si todo_anio es verdadero
    IF proc_todo_anio THEN
        -- Verificar si ya existe un registro con todo_anio verdadero
        SELECT idAnioModelo INTO idRegistro
        FROM anioModelos
        WHERE anioModeloInicio = 0 AND anioModeloFin = 0 AND todoAnio = TRUE
        LIMIT 1;
    ELSE
        -- Verificar si ya existe un registro con las mismas fechas
        SELECT idAnioModelo INTO idRegistro
        FROM anioModelos
        WHERE anioModeloInicio = proc_anio_inicio AND anioModeloFin = proc_anio_fin AND todoAnio = FALSE
        LIMIT 1;
    END IF;

    -- Si ya existe la relación, asignar el idAnioModelo existente
    IF idRegistro IS NOT NULL THEN
        SET anioexiste = TRUE;
        SELECT CONCAT('Existe el año en la tabla AnioModelo ', idRegistro) AS mensaje;
    ELSE
        -- Se registra el año del modelo
        INSERT INTO anioModelos (anioModeloInicio, anioModeloFin, todoAnio)
        VALUES (proc_anio_inicio, proc_anio_fin, proc_todo_anio);

        -- se guarda el id del registro 
        SET idRegistro = LAST_INSERT_ID();
        
        SET anioexiste = FALSE;
        
        SELECT CONCAT('El año a sido insertado correctamente ID: ', idRegistro) AS mensaje;
        
    END IF;

    -- Insertar la relación en modeloAnios si no existe
    IF anioexiste IS TRUE THEN
        
        SELECT idModeloAnio INTO idRegistroMA 
		  FROM modeloanios 
		  WHERE idModeloAnio = idRegistro 
		  AND idModelo = proc_modelo_id;
        
        SELECT CONCAT('Existe la relación del modelo con el año. ID: ', idRegistroMA) AS mensaje2;
        
    ELSE    
		  INSERT INTO modeloAnios (idModelo, idAnioModelo)
        VALUES (proc_modelo_id, idRegistro);
        
        SELECT CONCAT('La relacion a sido insertada del modelo con el año. ID: ', idRegistroMA) AS mensaje2;
    END IF;

END //

DELIMITER ;


DELIMITER //

CREATE OR REPLACE PROCEDURE InsertarModeloConAnio(
    IN proc_modelo_id INT,
    IN proc_anio_inicio INT,
    IN proc_anio_fin INT,
    IN proc_todo_anio BOOL
)
BEGIN

    DECLARE idRegistro INT DEFAULT NULL;
    DECLARE idRegistroMA INT DEFAULT NULL;
    DECLARE anioexiste BOOLEAN DEFAULT FALSE;

    -- Verificar si todo_anio es verdadero
    IF proc_todo_anio THEN
        -- Verificar si ya existe un registro con todo_anio verdadero
        SELECT idAnioModelo INTO idRegistro
        FROM anioModelos
        WHERE anioModeloInicio = 0 AND anioModeloFin = 0 AND todoAnio = TRUE
        LIMIT 1;
    ELSE
        -- Verificar si ya existe un registro con las mismas fechas
        SELECT idAnioModelo INTO idRegistro
        FROM anioModelos
        WHERE anioModeloInicio = proc_anio_inicio AND anioModeloFin = proc_anio_fin AND todoAnio = FALSE
        LIMIT 1;
    END IF;

    -- Si ya existe el año en la tabla anioModelos
    IF idRegistro IS NOT NULL THEN
        SET anioexiste = TRUE;
        SELECT CONCAT('Existe el año en la tabla AnioModelo ', idRegistro) AS mensaje;
    ELSE
        -- Insertar el año/rango en anioModelos
        INSERT INTO anioModelos (anioModeloInicio, anioModeloFin, todoAnio)
        VALUES (proc_anio_inicio, proc_anio_fin, proc_todo_anio);

        -- Obtener el idAnioModelo recién insertado
        SET idRegistro = LAST_INSERT_ID();
        
        SET anioexiste = FALSE;
        
        SELECT CONCAT('El año ha sido insertado correctamente ID: ', idRegistro) AS mensaje;
    END IF;

    -- Verificar si la relación ya existe
    IF anioexiste IS TRUE THEN
        SELECT idModeloAnio INTO idRegistroMA 
        FROM modeloAnios 
        WHERE idAnioModelo = idRegistro 
          AND idModelo = proc_modelo_id
        LIMIT 1;

        -- Si la relación existe, mostrar mensaje
        IF idRegistroMA IS NOT NULL THEN
            SELECT CONCAT('Existe la relación del modelo con el año. ID: ', idRegistroMA) AS mensaje2;
        ELSE
            -- Si no existe, insertar la relación
            INSERT INTO modeloAnios (idModelo, idAnioModelo)
            VALUES (proc_modelo_id, idRegistro);
            
            SET idRegistroMA = LAST_INSERT_ID();
            
            SELECT CONCAT('La relación ha sido insertada del modelo con el año. ID: ', idRegistroMA) AS mensaje2;
        END IF;
    ELSE
        -- Insertar la relación si el año es nuevo
        INSERT INTO modeloAnios (idModelo, idAnioModelo)
        VALUES (proc_modelo_id, idRegistro);
        
        SET idRegistroMA = LAST_INSERT_ID();
        
        SELECT CONCAT('La relación ha sido insertada del modelo con el año. ID: ', idRegistroMA) AS mensaje2;
    END IF;

END //

DELIMITER ;



describe modeloanios;

-- RELACONA LA TABLA MODELO AUTOPARTE CON EL MODELOANIO ... UTILIZADA
DELIMITER //

CREATE OR REPLACE PROCEDURE InsertarModeloAutoparte(
    IN p_idInventario INT,
    IN p_idModeloAnio INT
)
BEGIN
    -- Verificar si la relación entre modeloAnios y la autoparte ya existe en modeloAutopartes
    IF EXISTS (
        SELECT 1 
        FROM modeloAutopartes
        WHERE idModeloAnio = p_idModeloAnio 
          AND idInventario = p_idInventario
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La relación entre el autoparte y el modelo ya existe.';
    ELSE
        -- Insertar la relación en modeloAutopartes
        INSERT INTO modeloAutopartes (idModeloAnio, idInventario, estado)
        VALUES (p_idModeloAnio, p_idInventario, TRUE);
    END IF;
END //

DELIMITER ;

-- procedimiento almacenado que inserta un nuevo producto en la tabla inventarioAutoparte, registra la relación en proveedorProductos, y también en registroProductos,
DELIMITER //

CREATE OR REPLACE PROCEDURE InsertarProducto (
    IN p_idCategoria INT,
    IN p_idUnidadMedida INT,
    IN p_codigoBarras VARCHAR(50),
    IN p_nombreParte VARCHAR(100),
    IN p_descripcionParte VARCHAR(150),
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
    FROM inventarioAutoparte
    WHERE codigoBarras = p_codigoBarras AND estado = FALSE;

    -- Si el codigoBarras existe y tiene estado FALSE, actualizar el registro
    IF v_idInventario IS NOT NULL THEN
        UPDATE inventarioAutoparte
        SET idCategoria = p_idCategoria,
            idUnidadMedida = p_idUnidadMedida,
            nombreParte = p_nombreParte,
            descripcionParte = p_descripcionParte,
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
        INSERT INTO inventarioAutoparte (
            idCategoria, idUnidadMedida, codigoBarras, nombreParte, descripcionParte,
            cantidadActual, cantidadMinima, precioCompra, mayoreo, menudeo, colocado, urlImagen
        ) VALUES (
            p_idCategoria, p_idUnidadMedida, p_codigoBarras, p_nombreParte, p_descripcionParte,
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

CALL InsertarProducto(1, 1, '141f1fvffv1','MANIJA INTERIOR','DELANTERO DERECHO NEGRO',20,5,90,100.0,150.0,250.0,'',1,3);
CALL InsertarProducto(2, 1, '5454f5f45g5','MOTOR LIMPIAPARABRISA','12V',10,2,50.0,70.0,100.0,200.0,'http.hcf',2,3);
CALL InsertarProducto(idCategoria,idUnidadMedida, codigoBarras, p_nombreParte, descripcionParte, p_cantidadActual, p_cantidadMinima, precioCompra, 
	p_mayoreo, p_menudeo, p_colocado, urlImagen, idProveedor, idUsuario);
   
SELECT * FROM inventarioautoparte;
SELECT * FROM registroproductos;
SELECT * FROM proveedorproductos;

-- procedimiento almacenado que actualice el estado de un producto a FALSE en la tabla inventarioAutoparte 
-- y actualice el idUsuarioElimino y fechaElimino en la tabla registroProductos
DELIMITER //

CREATE PROCEDURE EliminarProducto (
    IN p_idInventario INT,
    IN p_idUsuario INT
)
BEGIN
    -- Actualizar el estado del producto a FALSE en inventarioAutoparte
    UPDATE inventarioAutoparte
    SET estado = FALSE
    WHERE idInventario = p_idInventario;

    -- Actualizar el idUsuarioElimino y fechaElimino en registroProductos
    UPDATE registroProductos
    SET idUsuarioElimino = p_idUsuario,
        fechaElimino = NOW()
    WHERE idInventario = p_idInventario;
END //

DELIMITER ;

CALL EliminarProducto(1,3)
EliminarProducto(idInventario, idUsuario)


-- ventas Paso 1: Crear una Venta
DELIMITER //

CREATE PROCEDURE CrearVenta (
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

CREATE PROCEDURE AgregarProductoVenta (
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
END //

DELIMITER ;

-- ventas Paso 3: Finalizar la Venta
DELIMITER //

CREATE PROCEDURE FinalizarVenta (
    IN p_idVenta INT,
    IN p_recibioDinero FLOAT,
    IN p_folioTicket VARCHAR(50),
    IN p_imprimioTicket BOOL,
    IN p_idTipoPago INT,
    IN p_referenciaUnica VARCHAR(50),
    IN p_descripcionPago VARCHAR(50)
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
    INSERT INTO pagoVenta (idVenta, idTipoPago, referenciaUnica, descripcionPago)
    VALUES (p_idVenta, p_idTipoPago, p_referenciaUnica, p_descripcionPago);
END //

DELIMITER ;

CALL CrearVenta(3,1);
CALL AgregarProductoVenta(1,1,2,'colocado',250);
CALL AgregarProductoVenta(1,2,3,'MENUDEO',100);
CALL FinalizarVenta(1,1000,'48f484c8f4c8f',TRUE,1,'NO APLICA','PAGADO');
CrearVenta (idUsuario, idCliente)
AgregarProductoVenta (idVenta, idInventario, cantidad, tipoVenta, precioVenta)
FinalizarVenta (idVenta, recibioDinero, folioTicket, imprimioTicket, idTipoPago, referenciaUnica, descripcionPago)

SELECT * FROM ventaProductos;
SELECT * FROM ventas;
SELECT * FROM pagoVenta;