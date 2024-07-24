# get_marca(id)
# VehiculosForm.cs
SELECT m.idMarca, m.nombre, count(mo.nombre) FROM marcas m JOIN modelos mo ON m.idMarca = mo.idMarca GROUP BY m.idMarca;

# get_modelo_anio_count(idmarca)
# Vehiculos_ModelosForm.cs
SELECT 
    ma.idModeloAnio, 
    m.nombre, 
    CONCAT(COALESCE(a.anioInicio, ''), '-', COALESCE(a.anioFin, '')) AS anioRango,
    COUNT(mp.idInventario) AS numProductos
FROM 
    modelos m
LEFT JOIN 
    modeloanios ma ON m.idModelo = ma.idModelo
LEFT JOIN 
    anios a ON ma.idAnio = a.idAnio
LEFT JOIN 
    modeloautopartes mp ON ma.idModeloAnio = mp.idModeloAnio
WHERE 
    m.idMarca = 11
GROUP BY 
    m.idModelo, a.idAnio
ORDER BY 
    m.nombre, ma.idModeloAnio;

# get_categorias
CategoriasForm.cs
SELECT 
    c.idCategoria, 
    c.nombre, 
    COUNT(i.idInventario) AS numProductos
FROM 
    categorias c
LEFT JOIN 
    inventario i ON c.idCategoria = i.idCategoria
GROUP BY 
    c.idCategoria, c.nombre
ORDER BY 
    c.idCategoria;
