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




































INSERT INTO modelos (idMarca, nombre) VALUES
(41, 'AVIATOR'),
(41, 'BLACKWOOD'),
(41, 'CONTINENTAL'),
(41, 'CORSAIR'),
(41, 'LS'),
(41, 'MARK'),
(41, 'MARK LT'),
(41, 'MILAN'),
(41, 'MKC'),
(41, 'MKS'),
(41, 'MKT'),
(41, 'MKX'),
(41, 'MKZ'),
(41, 'NAGIVATOR'),
(41, 'NAUTILUS'),
(41, 'NAVIGATOR'),
(41, 'TOWN CAR'),
(41, 'ZEPHYR');

INSERT INTO modelos (idMarca, nombre) VALUES
(42, 'CH613'),
(42, 'CHN'),
(42, 'CT'),
(42, 'CXU'),
(42, 'GRANITE'),
(42, 'GU GRANITE'),
(42, 'VHA'),
(42, 'VISION');

INSERT INTO modelos (idMarca, nombre) VALUES
(43, 'BUS'),
(43, 'TGX');

INSERT INTO modelos (idMarca, nombre) VALUES
(44, 'MP120MX');

INSERT INTO modelos (idMarca, nombre) VALUES
(45, '2'),
(45, '3'),
(45, '5'),
(45, '6'),
(45, '323'),
(45, '626'),
(45, '929'),
(45, 'B1600'),
(45, 'B2000'),
(45, 'B2200'),
(45, 'B2300'),
(45, 'B2400'),
(45, 'B2500'),
(45, 'B2600'),
(45, 'B3000'),
(45, 'B4000'),
(45, 'CRONOS'),
(45, 'CX-30'),
(45, 'CX-50'),
(45, 'CX3'),
(45, 'CX30'),
(45, 'CX5'),
(45, 'CX50'),
(45, 'CX7'),
(45, 'CX9'),
(45, 'MIATA'),
(45, 'MPV'),
(45, 'MX3'),
(45, 'MX5'),
(45, 'MX6'),
(45, 'NAVAJO'),
(45, 'PICK UP'),
(45, 'PROTEGE'),
(45, 'RX8'),
(45, 'TRIBUTE');

INSERT INTO modelos (idMarca, nombre) VALUES
(46, '709'),
(46, '909'),
(46, '971'),
(46, 'A220'),
(46, 'A250'),
(46, 'ACTROS'),
(46, 'AMG GT'),
(46, 'AMG GT 53'),
(46, 'AMG GT C'),
(46, 'B250'),
(46, 'B250E'),
(46, 'C180'),
(46, 'C200'),
(46, 'C220'),
(46, 'C230'),
(46, 'C232 AMG'),
(46, 'C240'),
(46, 'C280'),
(46, 'C300'),
(46, 'C320'),
(46, 'C350'),
(46, 'C350E'),
(46, 'C400'),
(46, 'C43 AMG'),
(46, 'C55 AMG'),
(46, 'C63 AMG'),
(46, 'CL500'),
(46, 'CL55 AMG'),
(46, 'CL600'),
(46, 'CL65 AMG'),
(46, 'CLA'),
(46, 'CLA200'),
(46, 'CLA250'),
(46, 'CLASE A'),
(46, 'CLASE B'),
(46, 'CLASE C'),
(46, 'CLASE C 180'),
(46, 'CLASE C 200'),
(46, 'CLASE C 300'),
(46, 'CLASE C 350'),
(46, 'CLASE E'),
(46, 'CLASE E320'),
(46, 'CLASE G'),
(46, 'CLASE GLA'),
(46, 'CLASE GLC'),
(46, 'CLASE GLE'),
(46, 'CLASE GLS'),
(46, 'CLASE M'),
(46, 'CLASE R'),
(46, 'CLASE S'),
(46, 'CLASE S400'),
(46, 'CLASE S550'),
(46, 'CLASE S600'),
(46, 'CLASE-M'),
(46, 'CLK'),
(46, 'CLK280'),
(46, 'CLK320'),
(46, 'CLK350'),
(46, 'CLK500'),
(46, 'CLK55 AMG'),
(46, 'CLS'),
(46, 'CLS500'),
(46, 'CLS53 AMG'),
(46, 'CLS55 AMG'),
(46, 'E-320'),
(46, 'E200'),
(46, 'E250'),
(46, 'E300'),
(46, 'E400'),
(46, 'E500'),
(46, 'EVOBUS'),
(46, 'GL'),
(46, 'GL320'),
(46, 'GL3400'),
(46, 'GL350'),
(46, 'GL450'),
(46, 'GL500'),
(46, 'GL550'),
(46, 'GLA'),
(46, 'GLA 200'),
(46, 'GLA180'),
(46, 'GLA200'),
(46, 'GLA250'),
(46, 'GLC'),
(46, 'GLC300'),
(46, 'GLC350e'),
(46, 'GLC43 AMG'),
(46, 'GLC63 AMG'),
(46, 'GLE'),
(46, 'GLE300D'),
(46, 'GLE350'),
(46, 'GLE400'),
(46, 'GLE43'),
(46, 'GLE43 AMG'),
(46, 'GLE450'),
(46, 'GLE450 AMG'),
(46, 'GLE500'),
(46, 'GLE53 AMG'),
(46, 'GLE550'),
(46, 'GLE550E'),
(46, 'GLE580'),
(46, 'GLE63 AMG'),
(46, 'GLE63 AMG S'),
(46, 'GLK'),
(46, 'GLS'),
(46, 'GLS450'),
(46, 'GLS550'),
(46, 'HPN 196'),
(46, 'IRIZAR I6'),
(46, 'ML'),
(46, 'ML 320'),
(46, 'ML 350'),
(46, 'ML 500'),
(46, 'ML250'),
(46, 'ML320'),
(46, 'ML350'),
(46, 'ML430'),
(46, 'ML450'),
(46, 'ML500'),
(46, 'ML550'),
(46, 'OC 500'),
(46, 'R320'),
(46, 'R500'),
(46, 'S350'),
(46, 'S430'),
(46, 'S450'),
(46, 'S500'),
(46, 'S55 AMG'),
(46, 'S560'),
(46, 'S600'),
(46, 'S65 AMG'),
(46, 'SL540'),
(46, 'SLK'),
(46, 'SLK 280'),
(46, 'SLK 350'),
(46, 'SLK280'),
(46, 'SPRINTER'),
(46, 'SPRINTER 2500'),
(46, 'SPRINTER 3500'),
(46, 'TRAVEGO S400'),
(46, 'VIANO'),
(46, 'VITO');

INSERT INTO modelos (idMarca, nombre) VALUES
(47, 'BOBCAT'),
(47, 'COLONY PARK'),
(47, 'COMET'),
(47, 'CONTOUR'),
(47, 'COUGAR'),
(47, 'GRAND MARQUIS'),
(47, 'MARAUDER'),
(47, 'MARINER'),
(47, 'MILAN'),
(47, 'MONARCH'),
(47, 'MONTAINEER'),
(47, 'MONTEGO'),
(47, 'MONTEREY'),
(47, 'MOUNTAINEER'),
(47, 'MYSTIQUE'),
(47, 'SABLE'),
(47, 'TEMPO'),
(47, 'TRACER'),
(47, 'UNIVERSAL'),
(47, 'VILLAGER');

INSERT INTO modelos (idMarca, nombre) VALUES
(48, 'GT'),
(48, 'HS'),
(48, 'MG'),
(48, 'MG5'),
(48, 'ONE'),
(48, 'RX5'),
(48, 'RX8'),
(48, 'ZS');

INSERT INTO modelos (idMarca, nombre) VALUES
(49, 'COOPER'),
(49, 'COOPER CHILI'),
(49, 'COOPER CLUBMAN'),
(49, 'COOPER COUNTRYMAN'),
(49, 'COOPER COUPE'),
(49, 'COOPER PACEMAN'),
(49, 'COOPER PEPPER'),
(49, 'COOPER S'),
(49, 'COUNTRYMAN'),
(49, 'MINI COOPER'),
(49, 'PACEMAN');

INSERT INTO modelos (idMarca, nombre) VALUES
(50, 'ASX'),
(50, 'ATTITUDE'),
(50, 'EAGLE'),
(50, 'ECLIPSE'),
(50, 'ECLIPSE CROSS'),
(50, 'ECLIPSE SPYDER'),
(50, 'ENDEAVOR'),
(50, 'FG25N'),
(50, 'GALANT'),
(50, 'GRANDIS'),
(50, 'L200'),
(50, 'LANCER'),
(50, 'MIRAGE'),
(50, 'MIRAGE G4'),
(50, 'MONTERO'),
(50, 'MONTERO SPORT'),
(50, 'OUTLANDER'),
(50, 'OUTLANDER PHEV'),
(50, 'OUTLANDER SPORT'),
(50, 'RAIDER'),
(50, 'RVR'),
(50, 'SPACE STAR'),
(50, 'SUMMIT'),
(50, 'TALON'),
(50, 'VAN'),
(50, 'XPANDER');

INSERT INTO modelos (idMarca, nombre)
VALUES (52, '510'),
       (52, '610'),
       (52, '710'),
       (52, '720'),
       (52, '200 SX'),
       (52, '200SX'),
       (52, '240 SX'),
       (52, '240SX'),
       (52, '300Z'),
       (52, '300ZX'),
       (52, '350Z'),
       (52, '370Z'),
       (52, 'ALMERA'),
       (52, 'ALTIMA'),
       (52, 'APRIO'),
       (52, 'ARMADA'),
       (52, 'AXXESS'),
       (52, 'B210'),
       (52, 'CABSTAR'),
       (52, 'CUBE'),
       (52, 'D21'),
       (52, 'D22'),
       (52, 'D23'),
       (52, 'DATSUN'),
       (52, 'ESTACAS'),
       (52, 'FG25N'),
       (52, 'FRONTIER'),
       (52, 'FRONTIER PRO-4X'),
       (52, 'FRONTIER V6 PRO-4X'),
       (52, 'GUAYIN'),
       (52, 'HARDBODY'),
       (52, 'HIKARI'),
       (52, 'ICHI VAN'),
       (52, 'ISHIVAN'),
       (52, 'JUKE'),
       (52, 'KICKS'),
       (52, 'KICKS E-POWER'),
       (52, 'KING CAB'),
       (52, 'LEAF'),
       (52, 'LUCINO'),
       (52, 'MARCH'),
       (52, 'MARCH ACTIVE'),
       (52, 'MAXIMA'),
       (52, 'MICRA'),
       (52, 'MURANO'),
       (52, 'NAVARA'),
       (52, 'NOTE'),
       (52, 'NP300'),
       (52, 'NV1500'),
       (52, 'NV200'),
       (52, 'NV2500'),
       (52, 'NV3500'),
       (52, 'NX'),
       (52, 'PATHFINDER'),
       (52, 'PICK UP D22'),
       (52, 'PLATINA'),
       (52, 'PULSAR'),
       (52, 'PULSAR NX'),
       (52, 'QUEST'),
       (52, 'ROGUE'),
       (52, 'ROGUE HYBRID'),
       (52, 'ROGUE SPORT'),
       (52, 'SAKURA'),
       (52, 'SAMURAI'),
       (52, 'SENTRA'),
       (52, 'STANZA'),
       (52, 'TIIDA'),
       (52, 'TITAN'),
       (52, 'TSUBAME'),
       (52, 'TSURU'),
       (52, 'TSURU I'),
       (52, 'TSURU II'),
       (52, 'TSURU III'),
       (52, 'TSURU SAMURAI'),
       (52, 'URVAN'),
       (52, 'V-DRIVE'),
       (52, 'VERSA'),
       (52, 'VERSA DRIVE'),
       (52, 'VERSA NOTE'),
       (52, 'VERSA V-DRIVE'),
       (52, 'X-TERRA'),
       (52, 'X-TRAIL'),
       (52, 'XTERRA'),
       (52, 'XTRAIL');

INSERT INTO modelos (idMarca, nombre)
VALUES (53, 'ACHIEVA'),
       (53, 'ALERO'),
       (53, 'AURORA'),
       (53, 'BRAVADA'),
       (53, 'BRVADA'),
       (53, 'CALAIS'),
       (53, 'CENTURY'),
       (53, 'CUTLASS'),
       (53, 'EIGHTY EIGHT'),
       (53, 'FIRENZA'),
       (53, 'INTRIGUE'),
       (53, 'NINETY EIGHT'),
       (53, 'OMEGA'),
       (53, 'SILHOUETTE'),
       (53, 'TORONADO'),
       (53, 'UNIVERSAL');

INSERT INTO modelos (idMarca, nombre)
VALUES (54, 'C5');

INSERT INTO modelos (idMarca, nombre)
VALUES (55, 'TIGRA');

INSERT INTO modelos (idMarca, nombre)
VALUES (56, '320'),
       (56, '325'),
       (56, '330'),
       (56, '335'),
       (56, '337'),
       (56, '340'),
       (56, '359'),
       (56, '365'),
       (56, '366'),
       (56, '367'),
       (56, '377'),
       (56, '378'),
       (56, '379'),
       (56, '384'),
       (56, '387'),
       (56, '567'),
       (56, 'T387'),
       (56, 'T600'),
       (56, 'T660'),
       (56, 'T800'),
       (56, 'UNIVERSAL');

INSERT INTO modelos (idMarca, nombre)
VALUES (57, '206'),
       (57, '207'),
       (57, '208'),
       (57, '301'),
       (57, '306'),
       (57, '307'),
       (57, '308'),
       (57, '405'),
       (57, '406'),
       (57, '407'),
       (57, '508'),
       (57, '2008'),
       (57, '3008'),
       (57, '5008'),
       (57, '207 CC'),  -- Handle spaces in names
       (57, '307 WAGON'),
       (57, 'EXPERT'),
       (57, 'GRAND RAID'),
       (57, 'MANAGER'),
       (57, 'PARTNER'),
       (57, 'PARTNER TEPEE'),
       (57, 'PROMASTER'),
       (57, 'RCZ'),
       (57, 'RIFTER');
