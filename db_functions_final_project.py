# === some database commands ======

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import messagebox
import pymysql
import os
import shutil
import db_config_file_final_project




class DatabaseError(Exception):
    def __init__(self, e):
        super().__init__(e)


def open_database():
    try:
        con = pymysql.connect(host=db_config_file_final_project.DB_SERVER,
                              user=db_config_file_final_project.DB_USER,
                              password=db_config_file_final_project.DB_PASS,
                              database=db_config_file_final_project.DB,
                              port=db_config_file_final_project.DB_PORT)

    except pymysql.InternalError as e:
        print(e)
        raise DatabaseError(e)
    except pymysql.OperationalError as e:
        print(e)
        raise DatabaseError(e)
    except pymysql.NotSupportedError as e:
        print(e)
        raise DatabaseError(e)
    finally:
        return con


def query_database(con, sql, values):
    try:
        cursor = con.cursor()
        cursor.execute(sql, values)
        rows = cursor.fetchall()
        num_of_rows = cursor.rowcount

    except pymysql.InternalError as e:
        print(e)
        raise DatabaseError(e)
    except pymysql.OperationalError as e:
        print(e)
        raise DatabaseError(e)
    except pymysql.ProgrammingError as e:
        print(e)
        raise DatabaseError(e)
    except pymysql.DataError as e:
        print(e)
        raise DatabaseError(e)
    except pymysql.IntegrityError as e:
        print(e)
        raise DatabaseError(e)
    except pymysql.NotSupportedError as e:
        print(e)
        raise DatabaseError(e)
    finally:
        cursor.close()
        con.close()
        return num_of_rows, rows


def insert_database(con, sql, vals):
    try:
        cursor = con.cursor()
        cursor.execute(sql, vals)
        con.commit()

    except pymysql.InternalError as e:
        raise DatabaseError(e)
    except pymysql.OperationalError as e:
        raise DatabaseError(e)
    except pymysql.ProgrammingError as e:
        raise DatabaseError(e)
    except pymysql.DataError as e:
        raise DatabaseError(e)
    except pymysql.IntegrityError as e:
        raise DatabaseError(e)
    except pymysql.NotSupportedError as e:
        raise DatabaseError(e)
    finally:
        cursor.close()
        con.close()

def search_records_research():

    try:
        con = pymysql.connect(host=db_config_file_final_project.DB_SERVER,
                              user=db_config_file_final_project.DB_USER,
                              password=db_config_file_final_project.DB_PASS,
                              database=db_config_file_final_project.DB,
                              port=db_config_file_final_project.DB_PORT)
        sql = "Select p.PI_FName, p.PI_LName, r.Research_Field" \
              "from pi p, pi_research pr, research r " \
              "where p.PI_ID = pr.PI_ID" \
              "and pr.Research_ID = r.Research_ID"
        print(sql)
        vals = options_var.get(), search_text_var.get()
        print(vals)
        cursor = con.cursor
        cursor.execute(sql,vals)
        rows_pi = cursor.fetchall()
        num_of_rows_pi = cursor.rowcount
        cursor.close()
        con.close()
    except:
        print("Error")
