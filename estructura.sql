-- AUTORES
-- Emanuel Pacheco Alberto
-- Leonel Federico Valencia Estudillo

-- CREACION DE LA BASE DE DATOS

CREATE OR REPLACE DATABASE el_gabacho;

-- USAR LA BASE DE DATOS

 USE el_gabacho
 
 -- CREACION DE LA TABLA ROLES ** OCULTO **
 
CREATE TABLE roles (
	idRol INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
   nombreRol VARCHAR(50) NOT NULL,
   descripcion VARCHAR(100)
);

 -- CREACION DE LA TABLA USUARIOS **
 
 CREATE TABLE usuarios (
  idUsuario INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
  idRol INT NOT NULL,
  nombreCompleto VARCHAR(50) NOT NULL,
  nombreUsuario VARCHAR(15) NOT NULL,
  contrasenia VARCHAR(15) NOT NULL,
  fechaCreacion timestamp default CURRENT_TIMESTAMP,
  estado bool default true,
  FOREIGN KEY (idRol) REFERENCES rol(idRol)
);

-- CREACION DE LA TABLA PROVEEDORES *

CREATE TABLE proveedores (
  idProveedor INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
  empresa VARCHAR(50) NOT NULL,
  nombreEncargado VARCHAR(50),
  telefono VARCHAR(10),
  correo varchar(50)
);

-- CREACION DE LA TABLA CATEGORIAS

CREATE TABLE categorias (
  idCategoria INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
  nombreCategoria VARCHAR(50) NOT NULL
);

-- CREACION DE LA TABLA UNIDAD MEDIDAS ** OCULTO ** = M/CM ó PQ/PZ

CREATE TABLE unidadMedidas (
  idUnidadMedida INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
  tipoMedida VARCHAR(8) NOT NULL,
  descripcionMedida VARCHAR(100)
);

-- CREACION DE LA TABLA TIPO PAGOS ** OCULTO ** = EFECTIVO, CARJETA, TRANSFERENCIA, DEPOSITO

CREATE TABLE tipoPagos (
	idTipoPago INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
   tipoPago VARCHAR(20) NOT NULL,
   descripcion varchar(100)
);

-- CREACION DE LA TABLA CLIENTES = PUBLICO GENERAL

CREATE TABLE clientes (
	idCliente INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
	nombreCliente VARCHAR(30) NOT NULL
);

-- CREACION DE LA TABLA MARCAS MODELOS Y AÑOS

-- CREACION DE LA TABLA MARCAS

CREATE TABLE marcas (
	idMarca INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
   nombreMarca VARCHAR(40) NOT NULL,
   urlLogo VARCHAR(300),
	estado BOOL DEFAULT TRUE
);

-- CREACION DE LA TABLA MODELOS

CREATE TABLE modelos (
	idModelo INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
   idMarca INT NOT NULL,
   nombre VARCHAR(50) NOT NULL,
   estado BOOL DEFAULT TRUE,
   FOREIGN KEY (idMarca) REFERENCES marca(idMarca)
);

-- CREACION DE LA TABLA AÑO MODELOS

CREATE TABLE anioModelos (
	idAnioModelo INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
   anioModeloInicio INT UNSIGNED NOT NULL,
   anioModeloFin INT UNSIGNED NOT NULL,
   todoAnio BOOL DEFAULT FALSE,
);

-- CREACION DE LA TABLA MODELO AÑOS "RELACION TABLA MODELOS Y AÑO MODELOS"

CREATE TABLE modeloAnios (
	idModeloAnio INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
	idModelo INT NOT NULL,
	idAnioModelo INT NOT NULL,
	estado BOOL DEFAULT TRUE
);

-- CREACION DE LA TABLA INVENTARIO AUTOPARTES

create table inventarioAutoparte (
	idInventarioA INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
   idCategoria INT,
   idUnidadMedidas INT UNSIGNED NOT NULL,
   codigoBarras VARCHAR(50) NOT NULL UNIQUE,
   nombreParte VARCHAR(100) NOT NULL,
   descripcionParte VARCHAR(150) NOT NULL,
   cantidadActual FLOAT UNSIGNED DEFAULT 0 NOT NULL,
   cantidadMinima FLOAT UNSIGNED DEFAULT 1 NOT NULL,
   precioCompra FLOAT UNSIGNED DEFAULT 0.00 NOT NULL,
   precioMenudeo FLOAT UNSIGNED DEFAULT 0.00 NOT NULL,
   precioMayoreo FLOAT UNSIGNED DEFAULT 0.00 NOT NULL,
   precioColocado FLOAT UNSIGNED DEFAULT 0.00 NOT NULL,
   urlImagen VARCHAR(300),
   estado BOOL DEFAULT TRUE,
   FOREIGN KEY (idCategoria) REFERENCES categorias(idCategoria),
   FOREIGN KEY (idUnidadMedidas) REFERENCES unidadMedidas(idUnidadMedida)
);

CREATE TABLE registroProductos (
  idregistroProducto INT auto_increment PRIMARY KEY,
  IdInventarioA INT,
  idUsuarioRegistro INT,
  fechaCreacion timestamp default CURRENT_TIMESTAMP,
  idUsuarioElimino INT,
  fechaElimino timestamp default CURRENT_TIMESTAMP,
  FOREIGN KEY (idUsuarioRegistro) REFERENCES usuarios(idUsuario),
  FOREIGN KEY (idUsuarioElimino) REFERENCES usuarios(idUsuario)
);

CREATE TABLE ventas (
  idVenta INT auto_increment primary key,
  idUsuario INT,
  idCliente INT,
  montoTotal FLOAT,
  recibioDinero FLOAT,
  folioTicket VAR,
  conceptoTicket BOOL,
  fechaVenta TIMESTAMP,
  estado BOOL default true,
  FOREIGN KEY (idUsuario) REFERENCES usuarios(idModeloAnio),
  FOREIGN KEY (idCliente) REFERENCES clientes(idCliente)
);



