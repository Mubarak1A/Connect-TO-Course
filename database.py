#!/usr/bin/python3
"""Database module to connect to the cloud database"""

from sqlalchemy import create_engine, text

db_username = "qlhg4f8i2v4k3hmr6i5x"
db_password = "pscale_pw_wsiMA95JpZsM8u6rkiZFXSbJf0bXt5TnebXHX2ctkFX"
db_host = "aws.connect.psdb.cloud"
db_name = "connecttocourse"

engine = create_engine("mysql+pymysql://{0}:{1}@{2}/{3}".format(db_username, db_password, db_host, db_name),
                       connect_args = {
                           "ssl": {
                               "ssl_ca": "/etc/ssl/cert.pem"
                           }
                       })

with engine.connect() as conn:
    result = conn.execute(text("select * from courses"))
    print(result.all())
