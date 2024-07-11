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

-- INSERCIONES A LA TABLA  marcas
INSERT INTO marcas (nombreMarca, urlLogo) VALUES
('ACURA','https://lofrev.net/wp-content/photos/2014/08/Acura-logo.gif'),
('ALFA ROMEO'),
('AMC'),
('AUDI','http://iuv.sdis86.net/wp-content/uploads/logos_constructeurs/audi_new-logo_09-e1437047622921.jpg'),
('BMW','https://logos-download.com/wp-content/uploads/2016/02/BMW_logo_big_transparent_png-700x700.png'),
('BUICK','https://keyautocompany.com/wp-content/uploads/2018/03/buick-logo.png'),
('CADILLAC'),
('CAMION'),
('CATERPILLAR'),
('CHANGAN'),
('CHEVROLET','http://iuv.sdis86.net/wp-content/uploads/logos_constructeurs/chevrolet.jpg'),
('CHIREY'),
('CHRYSLER','http://iuv.sdis86.net/wp-content/uploads/logos_constructeurs/Chrysler-logo-old1-800x440.png'),
('CUPRA'),
('DATSUN'),
('DINA','https://iconape.com/wp-content/files/tk/162664/png/dina-logo.png'),
('DODGE'),
('EAGLE'),
('FAW'),
('FIAT','http://iuv.sdis86.net/wp-content/uploads/logos_constructeurs/1024px-Fiat_Logo.svg_-150x150.png'),
('FORD','http://iuv.sdis86.net/wp-content/uploads/logos_constructeurs/car_logo_PNG1666-800x307.png'),
('FOTON'),
('FREIGHTLINER','https://cdn.shopify.com/s/files/1/1029/5377/products/FL_Logos_4_1024x1024.png?v=1496304150'),
('GMC'),
('HINO','https://aespares.wpenginepowered.com/wp-content/uploads/2017/07/Hino-logo-300x279.png'),
('HONDA','http://iuv.sdis86.net/wp-content/uploads/logos_constructeurs/honda_logo_3312.gif'),
('HUMMER'),
('HYSTER'),
('HYUNDAI','https://www.autonoviny.sk/wp-content/uploads/2013/03/HYUNDAI-LOGO7-213x213.png'),
('INFINITI'),
('INTERNATIONAL','https://logoeps.com/wp-content/uploads/2013/03/international-vector-logo.png'),
('ISUZU','http://iuv.sdis86.net/wp-content/uploads/2015/07/isuzu-cars-logo-emblem-800x581.jpg'),
('JAC'),
('JAGUAR'),
('JEEP'),
('KENWORTH','https://i.etsystatic.com/39729829/r/il/31b76d/4556513199/il_680x540.4556513199_8isf.jpg'),
('KIA','http://iuv.sdis86.net/wp-content/uploads/logos_constructeurs/kia-logo-hd-sk-png-800x466.png'),
('KOMATSU'),
('LAND ROVER','http://iuv.sdis86.net/wp-content/uploads/2015/09/Land-Rover-1.gif'),
('LEXUS'),
('LINCOLN'),
('MACK'),
('MAN'),
('MARCO POLO'),
('MAZDA','http://iuv.sdis86.net/wp-content/uploads/2015/07/mazda-logo-2400.gif'),
('MERCEDES BENZ','http://iuv.sdis86.net/wp-content/uploads/2015/07/Mercedes_Benz_logo-800x565.png'),
('MERCURY'),
('MG'),
('MINI'),
('MITSUBISHI','https://blueraymechanical.com/wp-content/uploads/2015/06/mitsubishi-277x300.png'),
('MOTO TAXI','https://media.slid.es/uploads/344625/images/1625283/Brand.png'),
('NISSAN','http://iuv.sdis86.net/wp-content/uploads/logos_constructeurs/b3779-nissan.gif'),
('OLDSMOBILE'),
('OMODA'),
('OPEL'),
('PETERBILT'),
('PEUGEOT'),
('PLYMOUTH'),
('PONTIAC'),
('PORSCHE'),
('RAM'),
('RAMBLER'),
('RENAULT','https://seeklogo.com/images/R/Renault-logo-6EF3576C2E-seeklogo.com.png'),
('SAAB','http://iuv.sdis86.net/wp-content/uploads/2015/07/saab_logo_3520.gif'),
('SATURN'),
('SCANIA','https://seeklogo.com/images/S/Scania-logo-264C3E18C4-seeklogo.com.png'),
('SCION'),
('SEAT','http://iuv.sdis86.net/wp-content/uploads/2015/07/seat_logo_rgb_highres-800x670.jpg'),
('SINOTRUCK'),
('SMART'),
('STERLING'),
('SUBARU','http://iuv.sdis86.net/wp-content/uploads/2015/07/Subaru-logo-and-wordmark-800x600.png'),
('SUZUKI','http://iuv.sdis86.net/wp-content/uploads/2015/07/suzuki-logo-e1440487741394.jpg'),
('TESLA'),
('TOYOTA','http://iuv.sdis86.net/wp-content/uploads/logos_constructeurs/toyota-logo.png'),
('UNIVERSAL','https://th.bing.com/th/id/OIP.KjfkfL8wAv0ihVRI1rfkZQHaBe?rs=1&pid=ImgDetMain'),
('VOLKSWAGEN','http://iuv.sdis86.net/wp-content/uploads/logos_constructeurs/Volkswagen_logo-150x150.png'),
('VOLVO','http://iuv.sdis86.net/wp-content/uploads/2015/07/image001-150x150.jpg'),
('YALE'),
('AUTOBUSES','https://images.vexels.com/media/users/3/128933/isolated/preview/b54944f7322722034cfda55e601b4f8d-travel-bus-round-icon.png?width=320');




