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
WHERE u.usuario = "Alma123" AND DATE(v.fechaVenta) BETWEEN "2024-07-14" AND "2024-07-25"
GROUP BY u.usuario;