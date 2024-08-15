class Config():
    debug= True
    mysql_Host='db:3306'
    mysql_user= 'root'
    mysql_password= 'root'
    mysql_db='el_gabacho'
    SECRET_KEY="SUPER SECRETO"

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+mysql_user+':'+mysql_password+'@'+mysql_Host+'/'+mysql_db


configuracion={
    'development':Config
}
