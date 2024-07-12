-- OBTENER LA MARCA, MODELO Y AÑO DE LA TABLA RELACIONAL ANIO MODELO AÑOS
-- Buscar por la marca: ejemplo: CHEVROLET

SELECT marcas.nombreMarca AS Marca, modelos.nombre AS Modelo, 
aniomodelos.anioModeloInicio AS Año_Inicio, aniomodelos.anioModeloFin AS Año_Fin
FROM marcas, modelos, aniomodelos, modeloanios
WHERE marcas.nombreMarca = 'CHEVROLET' AND 
modelos.idModelo = modeloanios.idModelo AND
aniomodelos.idAnioModelo = modeloanios.idAnioModelo;

-- Buscar por la marca y modelo: ejemplo: CHEVROLET, CHEVY

SELECT marcas.nombreMarca AS Marca, modelos.nombre AS Modelo, 
aniomodelos.anioModeloInicio AS Año_Inicio, aniomodelos.anioModeloFin AS Año_Fin
FROM marcas, modelos, aniomodelos, modeloanios
WHERE marcas.nombreMarca = 'CHEVROLET' AND 
modelos.idModelo = 'CHEVY' AND
aniomodelos.idAnioModelo = modeloanios.idAnioModelo;