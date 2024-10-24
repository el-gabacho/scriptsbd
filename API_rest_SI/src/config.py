class Config():
    debug= True
    mysql_Host='localhost:3306'
    mysql_user= 'admin'
    mysql_password= 'admin123'
    mysql_db='el_gabacho'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+mysql_user+':'+mysql_password+'@'+mysql_Host+'/'+mysql_db


configuracion={
    'development':Config
}

#IMAGE_ROOT_PATH = "/home/soygabacho/imagenes/productos"
#FILE_ROOT_PATH = "/home/soygabacho/archivos"
IMAGE_ROOT_PATH = "C:\\imagenes_el_gabacho\\productos"
FILE_ROOT_PATH = "C:\\imagenes_el_gabacho\\archivos"