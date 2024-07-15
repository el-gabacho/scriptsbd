-- ELIMINAR BASE DE DATOS

DROP DATABASE el_gabacho_prueba;

-- CREACION DE LA BASE DE DATOS

CREATE OR REPLACE DATABASE el_gabacho_prueba;

-- USAR LA BASE DE DATOS

 USE el_gabacho_prueba;
 
 
-- ////////////////////////////////////////////////////////////////////////////////
		-- 		TABLAS DE LA BASE DE DATOS

 -- CREACION DE LA TABLA MARCAS

CREATE TABLE marcas (
idMarca INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(50) NOT NULL UNIQUE,
urlLogo VARCHAR(300)
);

-- CREACION DE LA TABLA MODELOS

CREATE TABLE modelos (
idModelo INT AUTO_INCREMENT PRIMARY KEY,
idMarca INT NOT NULL,
nombre VARCHAR(50) NOT NULL UNIQUE,
FOREIGN KEY (idMarca) REFERENCES marcas(idMarca) ON DELETE CASCADE
);

-- CREACION DE LA TABLA AÑOS

CREATE TABLE anios (
idAnio INT AUTO_INCREMENT PRIMARY KEY,
anioInicio INT UNSIGNED NOT NULL DEFAULT 0,
anioFin INT UNSIGNED NOT NULL DEFAULT 0,
anioTodo BOOL DEFAULT FALSE NOT NULL
);

-- CREACION DE LA TABLA RELACION MODELOAÑOS "RELACION TABLA MODELOS Y AÑOS"

CREATE TABLE modeloAnios (
    idModeloAnio INT AUTO_INCREMENT PRIMARY KEY,
    idModelo INT NOT NULL,
    idAnio INT NOT NULL,
    FOREIGN KEY (idModelo) REFERENCES modelos(idModelo) ON DELETE CASCADE,
    FOREIGN KEY (idAnio) REFERENCES anios(idAnio)
);

-- CREACION DE LA TABLA INVENTARIO AUTOPARTE

CREATE OR REPLACE TABLE inventario (
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
   urlImagen VARCHAR(300),
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
	FOREIGN KEY (idInventario) REFERENCES inventario(idInventario) ON DELETE CASCADE
);

-- CREACION DE LA TABLA CATEGORIAS

CREATE OR REPLACE TABLE categorias (
  idCategoria INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL UNIQUE
);

-- CREACION DE LA TABLA UNIDAD MEDIDAS

CREATE OR REPLACE TABLE unidadMedidas (
  idUnidadMedida INT AUTO_INCREMENT PRIMARY KEY,
  tipoMedida VARCHAR(8) NOT NULL UNIQUE,
  descripcion VARCHAR(100)
);


-- ////////////////////////////////////////////////////////////////////////////////////////

-- ************* PARA CONSULTAS INSERCIONES Y DEMAS **********

-- INSERTAR MARCAS (nombreMarca y LogoURL)
INSERT INTO marcas (nombre, urlLogo) VALUES
('ACURA','https://lofrev.net/wp-content/photos/2014/08/Acura-logo.gif'),
('ALFA ROMEO', NULL),
('AMC', NULL);

-- Inserts para la tabla modelos (idModelo y nombre del modelo)
INSERT INTO modelos (idMarca, nombre) VALUES (1, 'CL');
INSERT INTO modelos (idMarca, nombre) VALUES (1, 'CSX');
INSERT INTO modelos (idMarca, nombre) VALUES (2, '1500');

-- INSERT año

INSERT INTO anios (anioInicio, anioFin, anioTodo) VALUES (2010,2012,FALSE);
INSERT INTO anios (anioInicio, anioFin, anioTodo) VALUES (2012,2014,FALSE);

-- relacionar modelo con año MANUAL SI LO PERMITE

INSERT INTO modeloanios (idModelo, idAnio) VALUES (1,1);
INSERT INTO modeloanios (idModelo, idAnio) VALUES (1,2);
INSERT INTO modeloanios (idModelo, idAnio) VALUES (2,1);

-- Relacionar modelo con un año
-- Parametros (idModelo, anioInicio, anioFin, todoAnio )
-- CALL proc_modelo_anio(proc_id_modelo, proc_anio_inicio, proc_anio_fin, proc_anio_todo)

CALL proc_modelo_anio(1, 2010, 2012, FALSE);
CALL proc_modelo_anio(1, 2012, 2014, FALSE);

CALL proc_modelo_anio(2, 2010, 2012, FALSE);
CALL proc_modelo_anio(2, 2012, 2014, FALSE);

CALL proc_modelo_anio(2, 2022, 2024, FALSE);
CALL proc_modelo_anio(2, 0, 0, TRUE);

CALL proc_modelo_anio(3, 2022, 2024, FALSE);
CALL proc_modelo_anio(3, 0, 0, TRUE);

-- NO EXISTE EL MODELO PERO EL AÑO SI

CALL proc_modelo_anio(4, 0, 0, TRUE);

-- Crear un autoparte de Inventario

INSERT INTO inventario(idCategoria, idUnidadMedida, codigoBarras, nombre, descripcion ) VALUES (1, 1,'0001','MANIJA INTERIOR','COLOR NEGRO');
INSERT INTO inventario(idCategoria, idUnidadMedida, codigoBarras, nombre, descripcion ) VALUES (2, 2,'0002','MANIJA INTERIOR','COLOR BLANCO');
INSERT INTO inventario(idCategoria, idUnidadMedida, codigoBarras, nombre, descripcion ) VALUES (3, 2,'0003','MANIJA INTERIOR','COLOR AZUL');
INSERT INTO inventario(idCategoria, idUnidadMedida, codigoBarras, nombre, descripcion ) VALUES (3, 1,'0004','MANIJA INTERIOR','COLOR AMARILLO');

-- Relacionar un modeloanio con un Autoparte del Inventario
-- CALL proc_modeloanios_con_autoparte(proc_id_inventario, proc_id_modeloAnio)

CALL proc_modeloanio_autoparte(1, 1); -- MARCA ACURA, MODELO = 1.CL
CALL proc_modeloanio_autoparte(1, 2); -- MARCA ACURA, MODELO = 1.CL
CALL proc_modeloanio_autoparte(1, 3); -- MARCA ACURA, MODELO = 2. CSX

CALL proc_modeloanio_autoparte(2, 1); -- MARCA ACURA, MODELO = 1.CL
CALL proc_modeloanio_autoparte(2, 7); -- MARCA ALFA ROMERO, MODELO = 1. 1500
CALL proc_modeloanio_autoparte(2, 8); -- MARCA ALFA ROMERO, MODELO = 1. 1500

CALL proc_modeloanio_autoparte(3, 1); -- MARCA ACURA, MODELO = 1.CL
CALL proc_modeloanio_autoparte(3, 2); -- MARCA ACURA, MODELO = 1.CL
CALL proc_modeloanio_autoparte(3, 3); -- MARCA ACURA, MODELO = 2. CSX

INSERT INTO categorias (nombre) VALUES ('ABRAZADERAS SUSPENSION');
INSERT INTO categorias (nombre) VALUES ('AJUSTADORES DE SUSPENSION');
INSERT INTO categorias (nombre) VALUES ('AJUSTE DE UNIDAD');

INSERT INTO unidadMedidas (tipoMedida, descripcion) VALUES 
    ('PQ/PZ', 'El criterio es por unidad'),
    ('M/CM', 'Si un producto se vende por centímetros o metros');
-- --------------------------------------------------
-- Consultar todas las tablas

SELECT * FROM marcas;

SELECT * FROM modelos;

SELECT * FROM anios;

SELECT * FROM modeloanios;

SELECT * FROM modeloautopartes;

SELECT * FROM inventario;

SELECT * FROM categorias;

SELECT * FROM unidadmedidas;

-- modelos con su marca

SELECT m.nombre AS MARCA, mo.nombre AS MODELO 
FROM marcas m
INNER JOIN modelos mo ON m.idMarca = mo.idMarca;

-- modelo con anios tabla relacional
SELECT 
    m.idMarca AS ID_MARCA, m.nombre AS Marca,
    mo.idModelo AS ID_MODELO, mo.nombre AS Modelo,
    a.idAnio AS ID_AÑO, a.anioInicio AS INICIO_AÑO, a.anioFin AS FIN_AÑO,
    ma.idModeloAnio AS ID_RELACION_MODELO_AÑOS
FROM 
    marcas m
INNER JOIN 
    modelos mo ON m.idMarca = mo.idMarca
INNER JOIN 
    modeloanios ma ON mo.idModelo = ma.idModelo
INNER JOIN 
    anios a ON ma.idAnio = a.idAnio
ORDER BY 
    ma.idModeloAnio;

-- modelos con autopartes
SELECT 
    m.idMarca AS ID_MARCA, m.nombre AS Marca,
    mo.idModelo AS ID_MODELO, mo.nombre AS Modelo,
    an.idAnio AS ID_AÑO, an.anioInicio AS INICIO_AÑO, an.anioFin AS FIN_AÑO,
    ma.idModeloAnio AS ID_RELACION_MODELO_AÑOS,
    i.idInventario AS ID_AUTOPARTE, i.codigoBarras AS CODIGO,
    map.idModeloAutoparte AS ID_MODELO_AUTOPARTE_RELACIONAL
FROM 
    marcas m
INNER JOIN 
    modelos mo ON m.idMarca = mo.idMarca
INNER JOIN 
    modeloanios ma ON mo.idModelo = ma.idModelo
INNER JOIN 
    anios an ON ma.idAnio = an.idAnio
INNER JOIN 
    modeloautopartes map ON ma.idModeloAnio = map.idModeloAnio
INNER JOIN 
    inventario i ON map.idInventario = i.idInventario
ORDER BY 
    map.idModeloAutoparte;

-- producto autoparte con categoria y sin categorias
SELECT 
    i.idInventario AS ID_INVENTARIO, i.codigoBarras AS CODIGO,
    c.idCategoria AS ID_CATE, c.nombre AS NOMBRE_CATE,
    um.idUnidadMedida AS ID_MEDIDA, um.tipoMedida AS TIPO
FROM 
    inventario i
LEFT JOIN 
    categorias c ON i.idCategoria = c.idCategoria
LEFT JOIN 
    unidadmedidas um ON i.idUnidadMedida = um.idUnidadMedida;

-- producto autoparte son categorias
SELECT 
    inventario.idInventario AS ID_INVENTARIO, 
    inventario.codigoBarras AS CODIGO,
    categorias.idCategoria AS ID_CATE, 
    categorias.nombre AS NOMBRE_CATE,
    unidadmedidas.idUnidadMedida AS ID_MEDIDA, 
    unidadmedidas.tipoMedida AS TIPO
FROM 
    inventario
LEFT JOIN 
    categorias ON inventario.idCategoria = categorias.idCategoria
LEFT JOIN 
    unidadmedidas ON inventario.idUnidadMedida = unidadmedidas.idUnidadMedida
WHERE 
    inventario.idCategoria IS NULL;

-- Eliminacion directa 

DELETE FROM marcas WHERE idMarca = 1;
DELETE FROM modelos WHERE idModelo = 1;
DELETE FROM modeloanios WHERE idModeloAnio = 8;
DELETE FROM modeloautopartes WHERE idModeloAutoparte = 1;
DELETE FROM categorias WHERE idCategoria = 2;
UPDATE inventario SET idCategoria = 1 WHERE idInventario = 3;
UPDATE inventario SET idUnidadMedida = 2 WHERE idInventario = 3;
DELETE FROM unidadMedidas WHERE idUnidadMedida = 1; -- NO PERMITE ELIMINAR DIRECTO POR LAS RELACIONES
DELETE FROM inventario WHERE idInventario = 2;

-- RESETEAR, ELIMINA FILAS Y EMPIEZA DESDE UNO
DELETE FROM marcas;
ALTER TABLE marcas AUTO_INCREMENT = 1;

DELETE FROM modelos;
ALTER TABLE modelos AUTO_INCREMENT = 1;

DELETE FROM anios;
ALTER TABLE anios AUTO_INCREMENT = 1;

DELETE FROM modeloanios;
ALTER TABLE modeloanios AUTO_INCREMENT = 1;

DELETE FROM inventario;
ALTER TABLE inventario AUTO_INCREMENT = 1;

DELETE FROM modeloautopartes;
ALTER TABLE modeloautopartes AUTO_INCREMENT = 1;

DELETE FROM categorias;
ALTER TABLE categorias AUTO_INCREMENT = 1;

DELETE FROM unidadMedidas;
ALTER TABLE unidadMedidas AUTO_INCREMENT = 1;

-- ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


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
DROP PROCEDURE proc_modeloanios_con_autoparte;
DROP PROCEDURE proc_modelo_con_anio;

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



-- PROCEDIMIENTO A VERIFICAR 


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




