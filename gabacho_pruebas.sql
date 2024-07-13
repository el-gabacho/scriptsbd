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
    -- idCategoria INT,
    -- idUnidadMedida INT NOT NULL,
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
    estado BOOL DEFAULT TRUE
    -- FOREIGN KEY (idCategoria) REFERENCES categorias(idCategoria),
    -- FOREIGN KEY (idUnidadMedida) REFERENCES unidadMedidas(idUnidadMedida)
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
ALTER TABLE modelos AUTO_INCREMENT = 1;

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
WHERE marcas.nombreMarca = 'ACURA' AND 
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
    IN modelo_id INT,
    IN anio_inicio INT,
    IN anio_fin INT,
    IN todo_anio BOOL
)
BEGIN
    DECLARE idAnioModelo INT;
    DECLARE relacion_existente BOOLEAN DEFAULT FALSE;

    -- Verificar si todo_anio es verdadero
    IF todo_anio THEN
        -- Verificar si ya existe un registro con todo_anio verdadero
        SELECT idAnioModelo INTO idAnioModelo
        FROM aniomodelos
        WHERE anioModeloInicio = 0 AND anioModeloFin = 0 AND todoAnio = TRUE;
        
        SELECT 'Ya existe un registro con todos los años (VERDADERO)' AS mensaje;
        
    ELSE
        -- Verificar si ya existe un registro con las mismas fechas
        SELECT idAnioModelo INTO idAnioModelo 
        FROM aniomodelos 
        WHERE anioModeloInicio = anio_inicio AND anioModeloFin = anio_fin AND todoAnio = FALSE;
        
        SELECT 'Ya existe un registro con las mismas fechas' AS mensaje;
        
    END IF;

    -- Si ya existe la relación, asignar el idAnioModelo existente
    IF idAnioModelo IS NOT NULL THEN
        SET relacion_existente = TRUE;
    ELSE
        -- Insertar un nuevo registro en la tabla anioModelos si no existe
        INSERT INTO anioModelos (anioModeloInicio, anioModeloFin, todoAnio)
        VALUES (anio_inicio, anio_fin, todo_anio);

        -- Obtener el idAnioModelo del nuevo registro insertado
        SET idAnioModelo = LAST_INSERT_ID();

        -- Insertar la relación en modeloAnios
        INSERT INTO modeloanios (idModelo, idAnioModelo)
        VALUES (modelo_id, idAnioModelo);

        SET relacion_existente = FALSE;
    END IF;

    -- Mostrar el mensaje según si la relación ya existía o se creó
    IF relacion_existente THEN
        SELECT 'Existe la relación del modelo con el año' AS mensaje;
    ELSE
        SELECT 'Modelo y año relacionado correctamente' AS mensaje;
    END IF;
    
END //

DELIMITER ;



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


