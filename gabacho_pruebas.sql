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

CREATE PROCEDURE InsertarProducto (
    IN p_idCategoria INT,
    IN p_idUnidadMedida INT,
    IN p_codigoBarras VARCHAR(50),
    IN p_nombreParte VARCHAR(100),
    IN p_descripcionParte VARCHAR(150),
    IN p_cantidadActual FLOAT UNSIGNED,
    IN p_cantidadMinima FLOAT UNSIGNED,
    IN p_precioCompra FLOAT UNSIGNED,
    IN p_mayoreo FLOAT UNSIGNED,
    IN p_menudeo FLOAT UNSIGNED,
    IN p_colocado FLOAT UNSIGNED,
    IN p_urlImagen VARCHAR(300),
    IN p_idProveedor INT,
    IN p_idUsuario INT
)
BEGIN
    -- Insertar el nuevo producto en inventarioAutoparte
    INSERT INTO inventarioAutoparte (
        idCategoria,
        idUnidadMedida,
        codigoBarras,
        nombreParte,
        descripcionParte,
        cantidadActual,
        cantidadMinima,
        precioCompra,
        mayoreo,
        menudeo,
        colocado,
        urlImagen
    ) VALUES (
        p_idCategoria,
        p_idUnidadMedida,
        p_codigoBarras,
        p_nombreParte,
        p_descripcionParte,
        p_cantidadActual,
        p_cantidadMinima,
        p_precioCompra,
        p_mayoreo,
        p_menudeo,
        p_colocado,
        p_urlImagen
    );
    
    -- Obtener el idInventario recién insertado
    SET @nuevo_idInventario = LAST_INSERT_ID();

    -- Insertar en proveedorProductos
    INSERT INTO proveedorProductos (
        idProveedor,
        idInventario
    ) VALUES (
        p_idProveedor,
        @nuevo_idInventario
    );

    -- Insertar en registroProductos
    INSERT INTO registroProductos (
        idInventario,
        idUsuarioRegistro
    ) VALUES (
        @nuevo_idInventario,
        p_idUsuario
    );
END //

DELIMITER ;

CALL InsertarProducto(1, 1, '141f1fvffv1','MANIJA INTERIOR','DELANTERO DERECHO NEGRO',20,5,90,100.0,150.0,250.0,'',1,3);
CALL InsertarProducto(idCategoria,idUnidadMedida, codigoBarras, p_nombreParte, descripcionParte, p_cantidadActual, p_cantidadMinima, precioCompra, p_mayoreo, p_menudeo,
   p_colocado, urlImagen, idProveedor, idUsuario);
   
SELECT * FROM inventarioautoparte;
SELECT * FROM registroproductos;
SELECT * FROM proveedorproductos;