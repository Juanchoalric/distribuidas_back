create table barrios(
	idBarrio int not null identity,
	nombre varchar(150) not null,
	constraint pk_barrios primary key (idBarrio),
)
create table vecinos(
	documento varchar(20) not null,
	nombre varchar(150) not null,
	apellido varchar(150) not null,
	direccion varchar(250) null, 
	codigoBarrio int null
	constraint pk_vecinos primary key (documento),
	constraint fk_vecinos_barrios foreign key (codigoBarrio) references barrios
)

create table sitios(
	idSitio int not null identity,
	latitud decimal(9,5),
	longitud decimal(9,5),
	calle varchar(150) null,
	numero int,
	entreCalleA varchar(150) null,
	entreCalleB varchar(150) null,
	descripcion varchar(300),
	aCargoDe varchar(200),
	apertura time,
	cierre time,
	comentarios text,
	constraint pk_sitios primary key (idSitio)
)

create table rubros(
	idRubro int not null identity,
	descripcion varchar(200) not null,
	constraint pk_rubros primary key (idRubro),
)

create table desperfectos(
	idDesperfecto int not null identity,
	descripcion varchar(200) not null,
	idRubro int null,
	constraint pk_desperfectos primary key (idDesperfecto)
)

create table reclamos(
	idReclamo int not null identity,
	documento varchar(20) not null,
	idSitio int not null,
	idDesperfecto int null,
	descripcion varchar(1000) null,
	estado varchar(30),
	IdReclamoUnificado int null
	constraint pk_reclamos primary key (idReclamo),
	constraint fk_reclamos_vecinos foreign key (documento) references vecinos,
	constraint fk_reclamos_sitios foreign key (idSitio) references sitios,
	constraint fk_reclamos_desperfectos foreign key (idDesperfecto) references sitios,
	constraint fk_reclamos_reclamos foreign key (IdReclamoUnificado) references reclamos,
)

create table movimientosReclamo(
	idMovimiento int not null identity,
	idReclamo int not null,
	responsable varchar(150) not null,
	causa varchar(1000) not null,
	fecha datetime default getDate(),
	constraint pk_movimientosReclamo primary key (idMovimiento),
	constraint fk_movimientosReclamo_reclamos foreign key (idReclamo) references reclamos	
)

create table denuncias(
	idDenuncias int not null identity,
	documento varchar(20) not null,
	idSitio int null,
	descripcion varchar(2000) null,
	estado varchar(150),
	aceptaResponsabilidad int not null,
	constraint pk_denuncias primary key (idDenuncias),
	constraint fk_denuncias_vecinos foreign key (documento) references vecinos,
	constraint fk_denuncias_sitios foreign key (idSitio) references sitios
)

create table movimientosDenuncia(
	idMovimiento int not null identity,
	idDenuncia int not null,
	responsable varchar(150) not null,
	causa varchar(4000) not null,
	fecha datetime default getDate(),
	constraint pk_movimientosReclamo primary key (idMovimiento),
	constraint fk_movimientosReclamo_reclamos foreign key (idDenuncia) references denuncias	
)

create table personal(
	legajo int not null identity,
	nombre varchar(150) not null,
	apellido varchar(150) not null,
	password varchar(40) not null,
	sector varchar(200) not null,
	cartegoria int,  --Los inspectores son categoria 8
	fechaIngreso datetime,
	constraint pk_personal primary key (legajo)
)