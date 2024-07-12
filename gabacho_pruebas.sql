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
    FOREIGN KEY (idMarca) REFERENCES marcas(idMarca)
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
    FOREIGN KEY (idModelo) REFERENCES modelos(idModelo),
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
    estado BOOL DEFAULT TRUE
    -- INDEX idx_idModeloAnio (idModeloAnio),
    -- INDEX idx_idInventario (idInventario)
);


-- INSERTAR MARCAS
INSERT INTO marcas (nombreMarca, urlLogo) VALUES
('ACURA','https://lofrev.net/wp-content/photos/2014/08/Acura-logo.gif'),
('ALFA ROMEO', NULL),
('AMC', NULL);

-- Inserts para la marca ACURA en la tabla modelos
INSERT INTO modelos (idMarca, nombre) VALUES (1, 'CL');
INSERT INTO modelos (idMarca, nombre) VALUES (1, 'CSX');
INSERT INTO modelos (idMarca, nombre) VALUES (1, 'EL');

-- Inserts para año
INSERT INTO aniomodelos (anioModeloInicio, anioModeloFin) VALUES (2010,2014);
INSERT INTO aniomodelos (anioModeloInicio, anioModeloFin) VALUES (2015,2020);
INSERT INTO aniomodelos (anioModeloInicio, anioModeloFin) VALUES (2021,2024);

-- Inserts para modelos años

INSERT INTO modeloanios (idModelo, idAnioModelo) VALUES (1,1);
INSERT INTO modeloanios (idModelo, idAnioModelo) VALUES (2,2);
INSERT INTO modeloanios (idModelo, idAnioModelo) VALUES (3,3);

-- CONSULTA ELIMINA CASCADA

SELECT marcas.nombreMarca AS Marca, marcas.estado AS EstadoMarca,
modelos.nombre AS Modelo, modelos.estado AS EstadoModelo,
modeloanios.estado AS ModeloAniosEstado,
aniomodelos.anioModeloInicio AS Año_Inicio, aniomodelos.anioModeloFin AS Año_Fin
FROM marcas, modelos, aniomodelos, modeloanios
WHERE marcas.nombreMarca = 'ACURA' AND 
modelos.idModelo = modeloanios.idModelo AND
aniomodelos.idAnioModelo = modeloanios.idAnioModelo;

UPDATE marcas SET estado = 0 WHERE nombreMarca = 'ACURA';

-- SIRVE PARA ELIMINAR EN CASCADA UNA MARCA

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

-- TRIGGER: ANTES DE INSERTAR UN MARCA, VALIDA SI EXISTE EL NOMBRE DE ESA MARCA.
-- CONDICIONES:
-- SI EXISTE EL NOMBRE DE LA MARCA Y NO PONE UN URL, ACTIVAR ESTATUS.
-- SI EXISTE EL NOMBRE DE LA MARCA Y INGRESA UN NUEVO URL, ACTIVAR ESTATUS Y ACTUALIZA EL CAMPO URL.
-- SI NO EXISTE EL NOMBRE DE LA MARCA Y SI INGRESA O NO INGRESA UN URL, CREALO.

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

-- Insertar o actualizar la marca
INSERT INTO marcas (nombreMarca, urlLogo)
VALUES ('ACURA', '')
ON DUPLICATE KEY UPDATE
    urlLogo = IF(VALUES(urlLogo) <> '', VALUES(urlLogo), urlLogo),
    estado = TRUE;

-- Insertar o actualizar la marca
INSERT INTO marcas (nombreMarca, urlLogo)
VALUES ('AUDI', '')
ON DUPLICATE KEY UPDATE
    urlLogo = IF(VALUES(urlLogo) <> '', VALUES(urlLogo), urlLogo),
    estado = TRUE;

SELECT * FROM marcas;







