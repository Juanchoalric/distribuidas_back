import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = "/home/juanchoalric/Desktop/distribuidas/database/distribuidas.db"

    sql_create_barrios_table = """ CREATE TABLE IF NOT EXISTS barrios (
                                        idBarrio integer NOT NULL PRIMARY KEY,
                                        nombre varchar(150) NOT NULL
                                    ); """

    sql_create_personal_table = """ CREATE TABLE IF NOT EXISTS personal (
                                        legajo integer NOT NULL PRIMARY KEY,
                                        nombre varchar(150) NOT NULL,
                                        apellido varchar(150) NOT NULL,
                                        password varchar(40) NOT NULL,
                                        sector varchar(200) NOT NULL,
                                        categoria int,
                                        fechaIngreso datetime
                                    ); """

    sql_create_vecinos_table = """CREATE TABLE IF NOT EXISTS vecinos (
                                    documento varchar(20) NOT NULL PRIMARY KEY,
                                    nombre varchar(150) NOT NULL,
                                    apellido varchar(150) NOT NULL,
                                    direccion varchar(250) NULL, 
                                    codigoBarrio integer NULL,
                                    FOREIGN KEY (codigoBarrio) REFERENCES barrios (idBarrio)
                                );"""

    sql_create_sitios_table = """CREATE TABLE IF NOT EXISTS sitios (
                                    idSitio integer NOT NULL PRIMARY KEY,
                                    latitud decimal(9,5),
                                    longitud decimal(9,5),
                                    calle varchar(150) NULL,
                                    numero integer,
                                    entreCalleA varchar(150) NULL,
                                    entreCalleB varchar(150) NULL,
                                    descripcion varchar(300),
                                    aCargoDe varchar(200),
                                    apertura TIME,
                                    cierre TIME,
                                    comentarios text
                                );"""
    
    sql_create_rubros_table = """CREATE TABLE IF NOT EXISTS rubros (
                                    idRubro integer NOT NULL PRIMARY KEY,
                                    descripcion varchar(200) NOT NULL
                                );"""

    sql_create_desperfectos_table = """CREATE TABLE IF NOT EXISTS desperfectos (
                                    idDesperfecto integer NOT NULL PRIMARY KEY,
                                    descripcion varchar(200) NOT NULL,
                                    idRubro integer NULL,
                                    FOREIGN KEY (idRubro) REFERENCES rubros (idRubro)
                                );"""

    
    sql_create_reclamos_table = """CREATE TABLE IF NOT EXISTS reclamos (
                                    idReclamo integer NOT NULL PRIMARY KEY,
                                    documento varchar(20) NOT NULL,
                                    idSitio integer NOT NULL,
                                    idDesperfecto integer NULL,
                                    descripcion varchar(1000) NULL,
                                    estado varchar(30),
                                    IdReclamoUnificado int NULL,
                                    FOREIGN KEY (documento) REFERENCES vecinos (documento),
                                    FOREIGN KEY (idSitio) REFERENCES sitios (idSitio),
                                    FOREIGN KEY (idDesperfecto) REFERENCES desperfecto (idDesperfecto),
                                    FOREIGN KEY (IdReclamoUnificado) REFERENCES reclamos (idReclamo)
                                );"""


    sql_create_movimientosReclamo_table = """CREATE TABLE IF NOT EXISTS movimientosReclamo (
                                    idMovimiento integer NOT NULL PRIMARY KEY,
                                    idReclamo integer NOT NULL,
                                    responsable varchar(150) NOT NULL,
                                    causa varchar(1000) NOT NULL,
                                    fecha datetime default CURRENT_DATE,
                                    FOREIGN KEY (idReclamo) REFERENCES reclamos (idReclamo)
                                    );"""

    sql_create_denuncias_table = """CREATE TABLE IF NOT EXISTS denuncias (
                                    idDenuncias integer NOT NULL PRIMARY KEY,
                                    documento varchar(20) NOT NULL,
                                    idSitio integer NULL,
                                    descripcion varchar(2000) NULL,
                                    estado varchar(150),
                                    aceptaResponsabilidad integer NOT NULL,
                                    FOREIGN KEY (documento) REFERENCES vecinos (documento),
                                    FOREIGN KEY (idSitio) REFERENCES sitios (idSitio)
                                    );"""
    

    sql_create_movimientosDenuncia_table = """CREATE TABLE IF NOT EXISTS movimientosDenuncia (
                                    idMovimiento integer NOT NULL PRIMARY KEY,
                                    idDenuncia integer NOT NULL,
                                    responsable varchar(150) NOT NULL,
                                    causa varchar(4000) NOT NULL,
                                    fecha datetime DEFAULT CURRENT_DATE,
                                    FOREIGN KEY (idDenuncia) REFERENCES denuncias (idDenuncia)
                                    );"""


    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        create_table(conn, sql_create_personal_table)
        create_table(conn, sql_create_vecinos_table)
        create_table(conn, sql_create_sitios_table)
        create_table(conn, sql_create_reclamos_table)
        create_table(conn, sql_create_rubros_table)
        create_table(conn, sql_create_denuncias_table)
        create_table(conn, sql_create_desperfectos_table)
        create_table(conn, sql_create_movimientosReclamo_table)
        create_table(conn, sql_create_movimientosDenuncia_table)
        create_table(conn, sql_create_barrios_table)


    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()