# get_info_productos
# mainForm.cs
SELECT 
    i.idInventario,
    GROUP_CONCAT(CONCAT(mc.nombre, ' ', m.nombre, ' ', COALESCE(a.anioInicio, ''), '-', COALESCE(a.anioFin, '')) SEPARATOR ', ') AS Aplicaciones,
    i.codigoBarras,
    i.nombre,
    i.descripcion,
    i.cantidadActual,
    p.empresa,
    i.precioCompra,
    um.tipoMedida,
    i.cantidadMinima,
    i.mayoreo,
    i.menudeo,
    i.colocado,
    c.nombre AS categoriaNombre
FROM 
    inventario i
JOIN 
    categorias c ON i.idCategoria = c.idCategoria
JOIN 
    unidadmedidas um ON i.idUnidadMedida = um.idUnidadMedida
JOIN 
    proveedorproductos pp ON i.idInventario = pp.idInventario
JOIN 
    proveedores p ON pp.idProveedor = p.idProveedor
LEFT JOIN 
    modeloautopartes mp ON i.idInventario = mp.idInventario
LEFT JOIN 
    modeloanios ma ON mp.idModeloAnio = ma.idModeloAnio
LEFT JOIN 
    modelos m ON ma.idModelo = m.idModelo
LEFT JOIN 
    marcas mc ON m.idMarca = mc.idMarca
LEFT JOIN 
    anios a ON ma.idAnio = a.idAnio
GROUP BY 
    i.idInventario;

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
# CategoriasForm.cs
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

# ProveedoresForm.cs
SELECT * FROM proveedores;

# UsuariosForm.cs
SELECT u.idUsuario, u.nombreCompleto, u.usuario, r.nombre, u.fechaCreacion
FROM usuarios u JOIN roles r ON u.idRol = r.idRol 
WHERE u.estado = TRUE;

# Inventario_StockBajo.cs
SELECT codigoBarras, nombre, descripcion, cantidadActual, cantidadMinima FROM inventario WHERE cantidadMinima > cantidadActual;

# Inventario_busquedaAvanzada.cs
SELECT 
    i.idInventario,
    i.codigoBarras,
    i.nombre,
    i.descripcion,
    i.cantidadActual,
    p.empresa,
    mc.nombre AS marca,
    m.nombre AS modelo,
    CONCAT(COALESCE(a.anioInicio, ''), '-', COALESCE(a.anioFin, '')) AS anioRango
FROM 
    inventario i
JOIN 
    categorias c ON i.idCategoria = c.idCategoria
JOIN 
    proveedorproductos pp ON i.idInventario = pp.idInventario
JOIN 
    proveedores p ON pp.idProveedor = p.idProveedor
LEFT JOIN 
    modeloautopartes mp ON i.idInventario = mp.idInventario
LEFT JOIN 
    modeloanios ma ON mp.idModeloAnio = ma.idModeloAnio
LEFT JOIN 
    modelos m ON ma.idModelo = m.idModelo
LEFT JOIN 
    marcas mc ON m.idMarca = mc.idMarca
LEFT JOIN 
    anios a ON ma.idAnio = a.idAnio
WHERE 
    i.codigoBarras LIKE "%DW01443GTN%" OR 
    i.nombre LIKE "%PARABRISAS%" OR
    i.descripcion LIKE "%SD/HB 2 Y 4 PTAS%" OR
    c.nombre LIKE "%PARABRISAS%" OR
    p.empresa LIKE "%RADEC%" OR
    mc.nombre LIKE "%CHEVROLET%" OR
    m.nombre LIKE "%ASTRA%" OR
    CONCAT(COALESCE(a.anioInicio, ''), '-', COALESCE(a.anioFin, '')) = "2001-2006"
GROUP BY 
    i.idInventario;

-- ventasForm.cs
SELECT v.folioTicket, p.referenciaUnica, t.tipoPago, v.montoTotal, v.fechaVenta, u.usuario 
FROM ventas v 
JOIN pagoventa p ON v.idVenta = p.idVenta
JOIN tipopagos t ON p.idTipoPago = t.idTipoPago
JOIN usuarios u ON v.idUsuario = u.idUsuario
WHERE u.usuario = "Alma123" AND DATE(v.fechaVenta) = "2024-07-25";

-- ventas_revertirForm.cs
SELECT v.idVentaProducto, i.codigoBarras, i.nombre, i.descripcion, v.precioVenta, v.cantidad, u.tipoMedida, v.subtotal, v.tipoVenta 
FROM ventaproductos v 
JOIN inventario i ON v.idInventario = i.idInventario
JOIN unidadmedidas u ON i.idUnidadMedida = u.idUnidadMedida
WHERE v.idVenta=1;

-- ventas_generalesForm.cs
SELECT u.usuario, sum(v.montoTotal), v.fechaVenta
FROM ventas v 
JOIN usuarios u ON v.idUsuario = u.idUsuario
WHERE DATE(v.fechaVenta) BETWEEN "2024-08-01" AND "2024-08-31"
GROUP BY u.usuario;

-- importar
SELECT idCategoria FROM categorias WHERE nombre = "PARABRISAS";
SELECT idProveedor FROM proveedores WHERE empresa = "RADEC";
SELECT idMarca FROM marcas WHERE nombre = "SUZUKI";
SELECT idModelo FROM modelos mo JOIN marcas ma ON mo.idMarca = ma.idMarca WHERE mo.nombre = "VITARA" AND mo.idMarca = 73;
SELECT idAnio FROM anios WHERE anioInicio = "1989" AND anioFin = "1998"; 
SELECT ma.idModeloAnio FROM modeloAnios ma JOIN modelos m ON ma.idModelo = m.idModelo WHERE ma.idAnio = 82 AND ma.idModelo = 1588;

-- obtener modelos
SELECT mo.idModelo, mo.nombre,
	GROUP_CONCAT(CONCAT(COALESCE(a.anioInicio, ''), '-', COALESCE(a.anioFin, '')) SEPARATOR ', ') AS anos
FROM modelos mo 
JOIN marcas m ON mo.idMarca = m.idMarca
LEFT JOIN modeloAnios ma ON mo.idModelo = ma.idModelo
LEFT JOIN anios a ON ma.idAnio = a.idAnio
WHERE m.idMarca = 11
GROUP BY mo.idModelo;

SELECT i.idInventario,
    GROUP_CONCAT(CONCAT(mc.nombre, ' ', m.nombre, ' ', COALESCE(a.anioInicio, ''), '-', COALESCE(a.anioFin, '')) SEPARATOR ', ') AS Aplicaciones,
FROM inventario i
LEFT JOIN modeloautopartes mp ON i.idInventario = mp.idInventario
LEFT JOIN modeloanios ma ON mp.idModeloAnio = ma.idModeloAnio
LEFT JOIN modelos m ON ma.idModelo = m.idModelo
LEFT JOIN marcas mc ON m.idMarca = mc.idMarca
LEFT JOIN anios a ON ma.idAnio = a.idAnio
GROUP BY i.idInventario;


SELECT 
    CONCAT(i.nombre, ' ', i.descripcion, ' ', c.nombre, ' ', GROUP_CONCAT(CONCAT(mc.nombre, ' ', m.nombre) SEPARATOR ', ')) AS productoCompleto,
    i.idInventario,
    i.codigoBarras,
    i.nombre,
    i.descripcion,
    c.nombre,
    im.imgRepresentativa
FROM 
    inventario i
JOIN 
    categorias c ON i.idCategoria = c.idCategoria
LEFT JOIN 
    modeloautopartes mp ON i.idInventario = mp.idInventario
LEFT JOIN 
    modeloanios ma ON mp.idModeloAnio = ma.idModeloAnio
LEFT JOIN 
    modelos m ON ma.idModelo = m.idModelo
LEFT JOIN 
    marcas mc ON m.idMarca = mc.idMarca
LEFT JOIN 
    anios a ON ma.idAnio = a.idAnio
LEFT JOIN imagenes im ON i.idInventario = im.idInventario
GROUP BY 
    i.idInventario
HAVING 
    productoCompleto LIKE '%manija%'
    AND productoCompleto LIKE '%interior%'
    AND productoCompleto LIKE '%chevrolet%';

SELECT m.idMarca, m.nombre, mo.idModelo, mo.nombre, a.anioInicio, a.anioFin, a.anioTodo 
FROM modeloAutopartes mp LEFT JOIN modeloanios ma ON mp.idModeloAnio=ma.idModeloAnio 
LEFT JOIN modelos mo ON ma.idModelo=mo.idModelo LEFT JOIN marcas m ON mo.idMarca=m.idMarca LEFT JOIN anios a ON ma.idAnio=a.idAnio
WHERE mp.idInventario=2;

# agregar los idInvetario de la imagenes temporales depues de ejecutar pruebasPython/save_images.py
INSERT INTO imagenes (idInventario, imgRepresentativa)
SELECT p1.idInventario, true
FROM inventario p1
JOIN punto_venta.tc_productos p2 ON p1.codigoBarras = p2.codigo_barras
WHERE p2.imagen IS NOT NULL;