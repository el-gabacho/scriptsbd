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