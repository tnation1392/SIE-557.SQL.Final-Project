__author__ = 'silvianittel'
__copyright__ = "Copyright 2022, SIE557"
__version__ = "1.0"
__date__ = "03/08/2022"

# Connect to the database

import pymysql
import db_config_file_final_project

try:
    con = pymysql.connect(host=db_config_file_final_project.DB_SERVER,
                          user=db_config_file_final_project.DB_USER,
                          password=db_config_file_final_project.DB_PASS,
                          database=db_config_file_final_project.DB,
                          port=db_config_file_final_project.DB_PORT)

except (Exception) as error:
    print("Error while fetching data from MYSQL", error)
    exit()
finally:
    print("successfully connected to database")


