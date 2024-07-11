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

-- INSERCIONES A LA TABLA CATEGORIAS

INSERT INTO categorias (nombreCategoria) VALUES ('ABRAZADERAS SUSPENSION');
INSERT INTO categorias (nombreCategoria) VALUES ('AJUSTADORES DE SUSPENSION');
INSERT INTO categorias (nombreCategoria) VALUES ('AJUSTE DE UNIDAD');
INSERT INTO categorias (nombreCategoria) VALUES ('ALERONES');
INSERT INTO categorias (nombreCategoria) VALUES ('ALMA FASCIAS');
INSERT INTO categorias (nombreCategoria) VALUES ('AMORTIGUADOR SUSPENSION');
INSERT INTO categorias (nombreCategoria) VALUES ('AMORTIGUADORES');
INSERT INTO categorias (nombreCategoria) VALUES ('ANTI-IMPACTOS');
INSERT INTO categorias (nombreCategoria) VALUES ('ARMOR ALL');
INSERT INTO categorias (nombreCategoria) VALUES ('BALERO BASE AMORTIGUADOR');
INSERT INTO categorias (nombreCategoria) VALUES ('BALERO DOBLE');
INSERT INTO categorias (nombreCategoria) VALUES ('BANDA POLY-V');
INSERT INTO categorias (nombreCategoria) VALUES ('BANDA TIEMPO');
INSERT INTO categorias (nombreCategoria) VALUES ('BARRA TENSORA');
INSERT INTO categorias (nombreCategoria) VALUES ('BASE AMORTIGUADOR');
INSERT INTO categorias (nombreCategoria) VALUES ('BASE Y BALERO DE AMORTIGUADOR');
INSERT INTO categorias (nombreCategoria) VALUES ('BASES');
INSERT INTO categorias (nombreCategoria) VALUES ('BIGOTERAS');
INSERT INTO categorias (nombreCategoria) VALUES ('BISAGRAS');
INSERT INTO categorias (nombreCategoria) VALUES ('BISELES');
INSERT INTO categorias (nombreCategoria) VALUES ('BOMBA DE AGUA');
INSERT INTO categorias (nombreCategoria) VALUES ('BOMBA DE DIRECCION HIDRAULICA');
INSERT INTO categorias (nombreCategoria) VALUES ('BRAZO AUXILIAR');
INSERT INTO categorias (nombreCategoria) VALUES ('BRAZO COMPENSADOR');
INSERT INTO categorias (nombreCategoria) VALUES ('BRAZO CONTROL');
INSERT INTO categorias (nombreCategoria) VALUES ('BRAZO FASCIA');
INSERT INTO categorias (nombreCategoria) VALUES ('BRAZO PITMAN');
INSERT INTO categorias (nombreCategoria) VALUES ('BRAZO PUENTE');
INSERT INTO categorias (nombreCategoria) VALUES ('BRAZOS DEFENSA');
INSERT INTO categorias (nombreCategoria) VALUES ('BUJE BRAZO');
INSERT INTO categorias (nombreCategoria) VALUES ('BUJE CREMALLERA');
INSERT INTO categorias (nombreCategoria) VALUES ('BUJE DE HORQUILLA');
INSERT INTO categorias (nombreCategoria) VALUES ('BUJE DE PUENTE');
INSERT INTO categorias (nombreCategoria) VALUES ('BUJE DE PUNTA');
INSERT INTO categorias (nombreCategoria) VALUES ('BUJE DIRECCION');
INSERT INTO categorias (nombreCategoria) VALUES ('BUJE EJE');
INSERT INTO categorias (nombreCategoria) VALUES ('BUJE INFERIOR');
INSERT INTO categorias (nombreCategoria) VALUES ('BUJE SUPERIOR');
INSERT INTO categorias (nombreCategoria) VALUES ('BUJE TIRANTE');
INSERT INTO categorias (nombreCategoria) VALUES ('BUJE TRANSMISION');
INSERT INTO categorias (nombreCategoria) VALUES ('BUJE TRASERO');
INSERT INTO categorias (nombreCategoria) VALUES ('BUJES DE SUSPENSION');
INSERT INTO categorias (nombreCategoria) VALUES ('BUJES Y PERNOS');
INSERT INTO categorias (nombreCategoria) VALUES ('CAJA DE DIRECCION');
INSERT INTO categorias (nombreCategoria) VALUES ('CALAVERAS');
INSERT INTO categorias (nombreCategoria) VALUES ('CAMARAS Y SENSORES');
INSERT INTO categorias (nombreCategoria) VALUES ('CHAPAS Y CILINDROS');
INSERT INTO categorias (nombreCategoria) VALUES ('CILINDROS DE IGNICION');
INSERT INTO categorias (nombreCategoria) VALUES ('CILINDROS DE PUERTA');
INSERT INTO categorias (nombreCategoria) VALUES ('CINCHOS Y SUJETADORES DE CABLE');
INSERT INTO categorias (nombreCategoria) VALUES ('COFRE');
INSERT INTO categorias (nombreCategoria) VALUES ('COMPLEMENTOS RADIADORES');
INSERT INTO categorias (nombreCategoria) VALUES ('CONDENSADOR');
INSERT INTO categorias (nombreCategoria) VALUES ('CONECTORES');
INSERT INTO categorias (nombreCategoria) VALUES ('CONTROLES');
INSERT INTO categorias (nombreCategoria) VALUES ('COPLE DE DIRECCION');
INSERT INTO categorias (nombreCategoria) VALUES ('CREMALLERAS DE DIRECCION');
INSERT INTO categorias (nombreCategoria) VALUES ('CUARTOS');
INSERT INTO categorias (nombreCategoria) VALUES ('CUBRE POLVO');
INSERT INTO categorias (nombreCategoria) VALUES ('DEFENSAS');
INSERT INTO categorias (nombreCategoria) VALUES ('DEPOSITO LIMPIABRISAS');
INSERT INTO categorias (nombreCategoria) VALUES ('DEPOSITO RECUPERADOR');
INSERT INTO categorias (nombreCategoria) VALUES ('ELEVADORES');
INSERT INTO categorias (nombreCategoria) VALUES ('ESPEJOS');
INSERT INTO categorias (nombreCategoria) VALUES ('ESTRIBOS');
INSERT INTO categorias (nombreCategoria) VALUES ('EXCENTRICOS');
INSERT INTO categorias (nombreCategoria) VALUES ('FAN CLUTCH');
INSERT INTO categorias (nombreCategoria) VALUES ('FAROS');
INSERT INTO categorias (nombreCategoria) VALUES ('FAROS NIEBLA');
INSERT INTO categorias (nombreCategoria) VALUES ('FASCIAS');
INSERT INTO categorias (nombreCategoria) VALUES ('FILTRO ACEITE');
INSERT INTO categorias (nombreCategoria) VALUES ('FLECHA HOMOCINETICA');
INSERT INTO categorias (nombreCategoria) VALUES ('FOCO UNIVERSAL');
INSERT INTO categorias (nombreCategoria) VALUES ('GOMA TORNILLO ESTABILIZADOR');
INSERT INTO categorias (nombreCategoria) VALUES ('GOMAS DE BARRA ESTABILIZADORA');
INSERT INTO categorias (nombreCategoria) VALUES ('GOMAS VARILLAS ESTABILIZADORAS');
INSERT INTO categorias (nombreCategoria) VALUES ('GRAPA DE PRESION');
INSERT INTO categorias (nombreCategoria) VALUES ('GRAPA DE TAPICERIA');
INSERT INTO categorias (nombreCategoria) VALUES ('GRAPA DOBLE P/PIJA Y TORNILLO');
INSERT INTO categorias (nombreCategoria) VALUES ('GRAPA MOLDURA');
INSERT INTO categorias (nombreCategoria) VALUES ('GRAPA PARABRISAS');
INSERT INTO categorias (nombreCategoria) VALUES ('GUIA FASCIA');
INSERT INTO categorias (nombreCategoria) VALUES ('HORQUILLAS INFERIORES DE SUSPENSIÓN');
INSERT INTO categorias (nombreCategoria) VALUES ('HORQUILLAS SUPERIORES DE SUSPENSION');
INSERT INTO categorias (nombreCategoria) VALUES ('HULES');
INSERT INTO categorias (nombreCategoria) VALUES ('INTERRUPTORES');
INSERT INTO categorias (nombreCategoria) VALUES ('JUEGOS');
INSERT INTO categorias (nombreCategoria) VALUES ('JUNTA FLECHA LADO RUEDA');
INSERT INTO categorias (nombreCategoria) VALUES ('KIT DE REBOTE Y CUBRE POLVO');
INSERT INTO categorias (nombreCategoria) VALUES ('KITS DE DISTRIBUCION');
INSERT INTO categorias (nombreCategoria) VALUES ('LIENZOS Y COSTADOS');
INSERT INTO categorias (nombreCategoria) VALUES ('MANGO');
INSERT INTO categorias (nombreCategoria) VALUES ('MANIJAS');
INSERT INTO categorias (nombreCategoria) VALUES ('MARCO PARRILLA');
INSERT INTO categorias (nombreCategoria) VALUES ('MARCO RADIADOR');
INSERT INTO categorias (nombreCategoria) VALUES ('MAZA DE RUEDA');
INSERT INTO categorias (nombreCategoria) VALUES ('MOLDURAS');
INSERT INTO categorias (nombreCategoria) VALUES ('MOTO-VENTILADOR');
INSERT INTO categorias (nombreCategoria) VALUES ('MUELAS PARA PIJA');
INSERT INTO categorias (nombreCategoria) VALUES ('PARRILLAS');
INSERT INTO categorias (nombreCategoria) VALUES ('PIJAS');
INSERT INTO categorias (nombreCategoria) VALUES ('PLUMA LIMPIAPARABRISAS');
INSERT INTO categorias (nombreCategoria) VALUES ('POLEA');
INSERT INTO categorias (nombreCategoria) VALUES ('PORTA PLACAS');
INSERT INTO categorias (nombreCategoria) VALUES ('PUERTAS');
INSERT INTO categorias (nombreCategoria) VALUES ('RADIADORES');
INSERT INTO categorias (nombreCategoria) VALUES ('RADIADORES MECANICOS');
INSERT INTO categorias (nombreCategoria) VALUES ('REJILLAS');
INSERT INTO categorias (nombreCategoria) VALUES ('REMACHES');
INSERT INTO categorias (nombreCategoria) VALUES ('RESORTE DE SUSPENSION');
INSERT INTO categorias (nombreCategoria) VALUES ('RETENEDORES');
INSERT INTO categorias (nombreCategoria) VALUES ('ROLLO MOLDURA');
INSERT INTO categorias (nombreCategoria) VALUES ('ROTULA INFERIOR');
INSERT INTO categorias (nombreCategoria) VALUES ('ROTULA SUPERIOR');
INSERT INTO categorias (nombreCategoria) VALUES ('ROTULA TRASERA');
INSERT INTO categorias (nombreCategoria) VALUES ('SALPICADEROS');
INSERT INTO categorias (nombreCategoria) VALUES ('SEGUROS BARRIL');
INSERT INTO categorias (nombreCategoria) VALUES ('SEGUROS DE PRESION');
INSERT INTO categorias (nombreCategoria) VALUES ('SEGUROS PARA VARILLA DE PTA');
INSERT INTO categorias (nombreCategoria) VALUES ('SOPORTE BARRA TENSORA');
INSERT INTO categorias (nombreCategoria) VALUES ('SOPORTE MOTOR');
INSERT INTO categorias (nombreCategoria) VALUES ('SPOYLER');
INSERT INTO categorias (nombreCategoria) VALUES ('SWITCH DE IGNICION');
INSERT INTO categorias (nombreCategoria) VALUES ('TAPA CAJA');
INSERT INTO categorias (nombreCategoria) VALUES ('TAPON DE ACEITE');
INSERT INTO categorias (nombreCategoria) VALUES ('TAPONES INTERIORES DE TAPICERIA');
INSERT INTO categorias (nombreCategoria) VALUES ('TENSOR');
INSERT INTO categorias (nombreCategoria) VALUES ('TERMINAL EXTERIOR/INTERIOR/BIELETA');
INSERT INTO categorias (nombreCategoria) VALUES ('TIRANTE');
INSERT INTO categorias (nombreCategoria) VALUES ('TOLVAS');
INSERT INTO categorias (nombreCategoria) VALUES ('TOMA AGUA');
INSERT INTO categorias (nombreCategoria) VALUES ('TOPES PARA COFRE');
INSERT INTO categorias (nombreCategoria) VALUES ('TORNILLO ESTABILIZADOR');
INSERT INTO categorias (nombreCategoria) VALUES ('TORNILLOS');
INSERT INTO categorias (nombreCategoria) VALUES ('TUBO ENFRIAMIENTO');
INSERT INTO categorias (nombreCategoria) VALUES ('TUERCA DE MARIPOSA');
INSERT INTO categorias (nombreCategoria) VALUES ('TUERCA RAPIDA Y DE PRESION');
INSERT INTO categorias (nombreCategoria) VALUES ('VAMPIRO PARA CRISTAL');
INSERT INTO categorias (nombreCategoria) VALUES ('VARILLA LATERAL');
INSERT INTO categorias (nombreCategoria) VALUES ('VARIOS');
INSERT INTO categorias (nombreCategoria) VALUES ('VARIOS LAMINA');
INSERT INTO categorias (nombreCategoria) VALUES ('VARIOS MICA');

SELECT * FROM categorias;

-- INSERCIONES A LA TABLA MARCA



