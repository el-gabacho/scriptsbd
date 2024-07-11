USE el_gabacho;

-- INSERCIONES A LA TABLA ROLES (SOLO 3 ROLES)

INSERT INTO roles (nombreRol, descripcion) VALUES ("ADMINISTRADOR","Usuario que tendra todos los privilegios");
INSERT INTO roles (nombreRol, descripcion) VALUES ("ALMACEN","Encargado y acceso a ciertas vistas que el admin");
INSERT INTO roles (nombreRol, descripcion) VALUES ("CAJERO","Solo es atender y realizar una venta");

SELECT * FROM roles;

-- INSERCIONES A LA TABLA USUARIOS CON LOS ROLES

INSERT INTO usuarios (idRol, nombreCompleto, nombreUsuario, contrasenia) VALUES (1, "Juan", "Juan123", "Juan123@");
INSERT INTO usuarios (idRol, nombreCompleto, nombreUsuario, contrasenia) VALUES (2, "Francisco", "Francisco123", "Francisco123@");
INSERT INTO usuarios (idRol, nombreCompleto, nombreUsuario, contrasenia) VALUES (3, "Alma", "Alma123", "Alma123@");

SELECT * FROM usuarios;

-- INSERCIONES A LA TABLA UNIDAD MEDIDAS (SOLO 2 TIPOS)

INSERT INTO unidadmedidas (tipoMedida, descripcionMedida) VALUES ("PQ / PZ","Conteo por unidad");
INSERT INTO unidadmedidas (tipoMedida, descripcionMedida) VALUES ("M / CM","Usa enteros y 2 decimales para agranel");

SELECT * FROM unidadmedidas;

-- INSERCIONES A LA TABLA TIPO PAGO (SOLO 4 TIPOS)

INSERT INTO tipopagos (tipoPago, descripcion) VALUES ("EFECTIVO","Pago hecho en el local");
INSERT INTO tipopagos (tipoPago, descripcion) VALUES ("TARJETA","Pago hecho en el local");
INSERT INTO tipopagos (tipoPago, descripcion) VALUES ("TRANSFERENCIA","Recibe foto de la tranferencia hecha");
INSERT INTO tipopagos (tipoPago, descripcion) VALUES ("DEPOSITO","Recibe foto del ticket del deposito hecha");

SELECT * FROM tipopagos;

-- INSERCIONES A LA TABLA 





