import pymysql
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import db_config_file_final_project
import db_functions_final_project as db
from PIL import ImageTk, Image
import os
import shutil

rows = None
num_of_rows = None
row_counter = 0
global blank_textboxes_tab_two
global blank_textboxes_tab_four



file_name = "default.png"
path = db_config_file_final_project.PHOTO_DIRECTORY + file_name
image_selected = False
image_file_name = None
file_to_copy = None
file_new_home = None

#####################################################################################################################
#TabOne Functions


def load_database_results():
    global rows
    global num_of_rows

    try:
        con = pymysql.connect(host=db_config_file_final_project.DB_SERVER,
                              user=db_config_file_final_project.DB_USER,
                              password=db_config_file_final_project.DB_PASS,
                              database=db_config_file_final_project.DB,
                              port=db_config_file_final_project.DB_PORT)

        sql = "Select PI_FName, PI_LName, r.Research_Field, c.Campus_City," \
              " p.photo from pi p, pi_research pr, research r, campus c, pi_campus pc " \
              "where p.PI_ID = pr.PI_ID and pr.Research_ID = r.Research_ID and p.PI_ID = pc.PI_ID " \
              "and pc.Campus_ID = c.Campus_ID order by p.PI_LName asc"
        cursor = con.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        num_of_rows = cursor.rowcount

        #for row in rows:
            #print(row)

        cursor.close()
        con.close()
        has_loaded_successfully = True
        messagebox.showinfo("Connected to Database", "DB Initialization OK")

    except pymysql.InternalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.OperationalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.ProgrammingError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.DataError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.IntegrityError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.NotSupportedError as e:
        has_loaded_successfully = database_error(e)

    return has_loaded_successfully


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


def scroll_forward():
    global row_counter
    global num_of_rows
    global rows

    if row_counter >= (num_of_rows - 1):
            messagebox.showinfo("Database Error", "End of database")
    else:
        row_counter = row_counter + 1
        fPIFname.set(rows[row_counter][0])
        fPILname.set(rows[row_counter][1])
        fResearch.set(rows[row_counter][2])
        fCampus.set(rows[row_counter][3])

        try:
            ph_path = db_config_file_final_project.PHOTO_DIRECTORY + rows[row_counter][4]
            load_photo_tab_one(ph_path)
        except FileNotFoundError:
            load_photo_tab_one(db_config_file_final_project.PHOTO_DIRECTORY + "default.png")


def scroll_back():
    global row_counter
    global num_of_rows

    if row_counter == 0:
        messagebox.showinfo("Database Error", "Start of database")
    else:
        row_counter = row_counter -1
        fPIFname.set(rows[row_counter][0])
        fPILname.set(rows[row_counter][1])
        fResearch.set(rows[row_counter][2])
        fCampus.set(rows[row_counter][3])

    try:
        ph_path = db_config_file_final_project.PHOTO_DIRECTORY + rows[row_counter][4]
        load_photo_tab_one(ph_path)
    except FileNotFoundError:
        load_photo_tab_one(db_config_file_final_project.PHOTO_DIRECTORY + "default.png")
######################################################################################################################
#TabTwo Functions


def add_new_record():
    global blank_textboxes_tab_two
    blank_textbox_count = 0

    if PIFnameEntryTabTwo.get() == "":
        blank_textbox_count = blank_textbox_count + 1

    if PILnameEntryTabTwo.get() == "":
        blank_textbox_count = blank_textbox_count + 1

    if blank_textbox_count > 0:
        blank_textboxes_tab_two = True
        messagebox.showinfo("Database Error", "Blank Text boxes")
    elif blank_textbox_count == 0:
        blank_textboxes_tab_two = False
        try:
            insert_into_database(PIFnameEntryTabTwo.get(), PILnameEntryTabTwo.get())
        except Exception as e:
            messagebox.showinfo("Database Error", e)

        messagebox.showinfo("Database", "Record Added to Database")


def insert_into_database(fPIFName, fPILName):
    try:
        con = db.open_database()

    except Exception as e:
        messagebox.showinfo("Database connection error", e)
        exit()

    try:
         sql = "INSERT INTO pi(PI_FName, PI_LName) VALUES (%s,%s)"
         vals = (fPIFName, fPILName)
         db.insert_database(con, sql, vals)

    except Exception as e:
        messagebox.showinfo("Error inserting record in database")
        raise db.DatabaseError(e)

#####################################################################################################################
def on_tab_selected(event):

    global blank_textboxes_tab_two
    global blank_textboxes_tab_four

    selected_tab = event.widget.select()
    tab_text = event.widget.tab(selected_tab, "text")
    if tab_text == "PI/Research":

        if blank_textboxes_tab_two is False:
            load_database_results()

    if tab_text == "Add PI":
        blank_textboxes_tab_four = True

    if tab_text == "Postdoc":
            load_database_results2

    if tab_text == "Add Postdoc":
        blank_textboxes_tab_four = True





def insert_database(con, sql, vals):
    try:
        cursor = con.cursor()
        cursor.execute(sql, vals)
        con.commit()

    except pymysql.InternalError as e:
        raise db.DatabaseError(e)
    except pymysql.OperationalError as e:
        raise db.DatabaseError(e)
    except pymysql.ProgrammingError as e:
        raise db.DatabaseError(e)
    except pymysql.DataError as e:
        raise db.DatabaseError(e)
    except pymysql.IntegrityError as e:
        raise db.DatabaseError(e)
    except pymysql.NotSupportedError as e:
        raise db.DatabaseError(e)
    finally:
        cursor.close()
        con.close()
####################################################################################################################
#Tab3 Functions

def load_database_results2():
    global rows
    global num_of_rows

    try:
        con = pymysql.connect(host=db_config_file_final_project.DB_SERVER,
                              user=db_config_file_final_project.DB_USER,
                              password=db_config_file_final_project.DB_PASS,
                              database=db_config_file_final_project.DB,
                              port=db_config_file_final_project.DB_PORT)

        sql = "select p.PI_LName, po.Phd_Fname, po.Phd_Lname" \
              "from pi p, pi_postdoc pp, postdoc po" \
              "where p.PI_ID = pp.PI_ID and pp.Phd_ID = po.Phd_ID" \
              "order by po.Phd_Lname asc"
        cursor = con.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        num_of_rows = cursor.rowcount

        #for row in rows:
            #print(row)

        cursor.close()
        con.close()
        has_loaded_successfully = True
        messagebox.showinfo("Connected to Database", "DB Initialization OK")

    except pymysql.InternalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.OperationalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.ProgrammingError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.DataError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.IntegrityError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.NotSupportedError as e:
        has_loaded_successfully = database_error(e)

    return has_loaded_successfully


#######################################################################################################################
def add_new_record_phd():
    global blank_textboxes_tab_four
    blank_textbox_count = 0

    if PhdFnameEntryTabFour.get() == "":
        blank_textbox_count = blank_textbox_count + 1

    if PhdLnameEntryTabFour.get() == "":
        blank_textbox_count = blank_textbox_count + 1

    if blank_textbox_count > 0:
        blank_textboxes_tab_four = True
        messagebox.showinfo("Database Error", "Blank Text boxes")
    elif blank_textbox_count == 0:
        blank_textboxes_tab_four = False
        try:
            insert_into_database_phd(PhdFnameEntryTabFour.get(), PhdLnameEntryTabFour.get())
        except Exception as e:
            messagebox.showinfo("Database Error", e)

        messagebox.showinfo("Database", "Record Added to Database")


def insert_into_database_phd(fPhdFName, fPhdLName):
    try:
        con = db.open_database()

    except Exception as e:
        messagebox.showinfo("Database connection error", e)
        exit()

    try:
        sql = "INSERT INTO postdoc(Phd_FName, Phd_LName) VALUES (%s,%s)"
        vals = (fPhdFName, fPhdLName)
        db.insert_database(con, sql, vals)

    except Exception as e:
        messagebox.showinfo("Error inserting record in database")
        raise db.DatabaseError(e)

########################################################################################################################
#Photo Handling


def image_path(file_path):

    print(file_path)
    open_image = Image.open(file_path)
    image = ImageTk.PhotoImage(open_image)
    return image


def load_photo_tab_one(file_path):

    image = image_path(file_path)
    imgLabelTabOne.configure(image=image)
    imgLabelTabOne.image = image
#######################################################################################################################
#Tab5 Functions


def load_db_menu_research():
    try:
        con = db.open_database()

        sql = "SELECT Research_Field FROM research order by Research_Field asc"
        cursor = con.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        num_of_rows = cursor.rowcount

        researchList = []
        for row in rows:
            data = "%s" % (row[0])
            researchList.append(data)

        cursor.close()
        con.close()
        messagebox.showinfo("Connected to Database", "DB Connection OK")

    except pymysql.InternalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.OperationalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.ProgrammingError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.DataError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.IntegrityError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.NotSupportedError as e:
        has_loaded_successfully = database_error(e)

    return researchList


def search_records_r():
    global rows
    global num_of_rows

    research = (options_r.get())
    research = research.replace("'", "")

    try:
        con = pymysql.connect(host=db_config_file_final_project.DB_SERVER,
                              user=db_config_file_final_project.DB_USER,
                              password=db_config_file_final_project.DB_PASS,
                              database=db_config_file_final_project.DB,
                              port=db_config_file_final_project.DB_PORT)

        sql = "select p.PI_FName, p.PI_LName, r.Research_Field " \
              "from pi p, pi_research pr, research r " \
              "where p.PI_ID = pr.PI_ID and pr.Research_ID = r.Research_ID " \
              "and r.Research_Field=%s"

        print(sql)
        values = research
        num_of_rows, rows = db.query_database(con, sql, values)

    except db.DatabaseError:
        messagebox.showinfo("Error querying the database")
        raise Exception

def display_query_results():

    global rows
    global num_of_rows

    try:
        rows, num_of_rows = search_records_r()

    except Exception as e:
        pass

    table = ttk.Treeview(tab5, columns=(1, 2, 3), height=10, show="headings")

    table.heading(1, text="First Name")
    table.heading(2, text="Last Name")
    table.heading(3, text="Research Field")

    table.column(1, width=150)
    table.column(2, width=150)
    table.column(3, width=250)

    table.grid(row=1, column=0, columnspan=3, padx=15, pady=15)

    if success:
        if num_of_rows == 0:
            messagebox.showinfo("Database Error", "No results")

        else:
            for row in rows:
                print(row)
                table.insert('', 'end', values=(row[0], row[1], row[2]))

#####################################################################################################################
###############################################################################################################


form = tk.Tk()
form.title("Jackson Laboratory Lab Database")
form.geometry("800x500")
tab_parent = ttk.Notebook(form)

tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)
tab3 = ttk.Frame(tab_parent)
tab4 = ttk.Frame(tab_parent)
tab5 = ttk.Frame(tab_parent)# Create a style
style = ttk.Style(form)
style.theme_use('classic')


tab_parent.bind("<<NotebookTabChanged>>", on_tab_selected)

tab_parent.add(tab1, text="PI/Research")
tab_parent.add(tab2, text="Add PI")
tab_parent.add(tab3, text="Postdoc")
tab_parent.add(tab4, text="Add Postdoc")
tab_parent.add(tab5, text="Search by Research")

tab_parent.pack(expand=1, fill='both')

#StringVars

fPIFname = tk.StringVar()
fPILname = tk.StringVar()
fResearch = tk.StringVar()
fPhdFname = tk.StringVar()
fPhdLname = tk.StringVar()
fCampus = tk.StringVar()

##################################################################################################################

# Tab1 Widgets

FnameLabelTabOne = tk.Label(tab1, text="PI First Name")
LnameLabelTabOne = tk.Label(tab1, text="PI Last Name")
ResearchLabelTabOne = tk.Label(tab1, text="Research Focus")
CampusLabelTabOne = tk.Label(tab1, text="Campus")

LabnameEntryTabOne = tk.Entry(tab1)
FnameEntryTabOne = tk.Entry(tab1, textvariable=fPIFname)
LnameEntryTabOne = tk.Entry(tab1, textvariable=fPILname)
ResearchEntryTabOne = tk.Entry(tab1, textvariable=fResearch, width=35)
CampusEntryTabOne = tk.Entry(tab1, textvariable=fCampus)

imgTabOne = image_path(path)
imgLabelTabOne = tk.Label(tab1, image=imgTabOne)

buttonForward = tk.Button(tab1, text="Forward", command=scroll_forward)
buttonBack = tk.Button(tab1, text="Back", command=scroll_back)



#Tab1 Layout

FnameLabelTabOne.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
FnameEntryTabOne.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

LnameLabelTabOne.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
LnameEntryTabOne.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

ResearchLabelTabOne.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
ResearchEntryTabOne.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)

CampusLabelTabOne.grid(row=3, column=1,padx=5,pady=5, sticky=tk.W)
CampusEntryTabOne.grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)

imgLabelTabOne.grid(row=0, column=5, rowspan=6, columnspan=1, sticky=tk.E)

buttonBack.grid(row=5, column=1, rowspan=1, padx=15, pady=15)
buttonForward.grid(row=5, column=2, rowspan=1, padx=15, pady=15)

tab_parent.pack(expand=1, fill='both')

###################################################################################################################

#Tab2 Widgets

PIFnameLabelTabTwo = tk.Label(tab2, text="PI First Name")
PILnameLabelTabTwo = tk.Label(tab2, text="PI Last Name")


PIFnameEntryTabTwo = tk.Entry(tab2)
PILnameEntryTabTwo = tk.Entry(tab2)

buttonCommit = tk.Button(tab2, text="Add record to Database", command=add_new_record)

#Tab2 Layout


PIFnameLabelTabTwo.grid(row=2, column=0, padx=5, pady=10,sticky=tk.W)
PIFnameEntryTabTwo.grid(row=2, column=1, padx=5, pady=10, sticky=tk.W)

PILnameLabelTabTwo.grid(row=3, column=0, padx=5, pady=10, sticky=tk.W)
PILnameEntryTabTwo.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)


buttonCommit.grid(row=7, column=0, rowspan=3, padx=15, pady=15)


##################################################################################################################
#Tab 3 Widgets
PhdFnameLabelTabThree = tk.Label(tab3, text="Postdoc First Name")
PhdLnameLabelTabThree = tk.Label(tab3, text="Postdoc Last Name")
PInameLabelTabThree = tk.Label(tab3, text="Associated PI")
buttonForward2 = tk.Button(tab3, text="Forward")
buttonBack2 = tk.Button(tab3, text="Back")

PhdFnameEntryTabThree = tk.Entry(tab3, textvariable=fPhdFname)
PhdLnameEntryTabThree = tk.Entry(tab3, textvariable=fPhdLname)
PInameEntryTabThree = tk.Entry(tab3, textvariable=fPILname)

#Tab3 Layout
PhdFnameLabelTabThree.grid(row=2, column=0, padx=5, pady=10, sticky=tk.W)
PhdFnameEntryTabThree.grid(row=2, column=1, padx=5, pady=10, sticky=tk.W)

PhdLnameLabelTabThree.grid(row=3, column=0, padx=5, pady=10, sticky=tk.W)
PhdLnameEntryTabThree.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

PInameLabelTabThree.grid(row=4, column=0, padx=5, pady=10, sticky=tk.W)
PInameEntryTabThree.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

buttonForward2.grid(row=5, column=1, padx=15, pady=15)
buttonBack2.grid(row=5, column=0, padx=15, pady=15)

tab_parent.pack(expand=1, fill='both')


####################################################################################################################
#Tab4

PhdFnameLabelTabFour = tk.Label(tab4, text="Postdoc First Name")
PhdLnameLabelTabFour = tk.Label(tab4, text="Postdoc Last Name")


PhdFnameEntryTabFour = tk.Entry(tab4)
PhdLnameEntryTabFour = tk.Entry(tab4)

buttonCommit2 = tk.Button(tab4, text="Add record to Database", command=add_new_record_phd)

#Tab4 Layout


PhdFnameLabelTabFour.grid(row=2, column=0, padx=5, pady=10,sticky=tk.W)
PhdFnameEntryTabFour.grid(row=2, column=1, padx=5, pady=10, sticky=tk.W)

PhdLnameLabelTabFour.grid(row=3, column=0, padx=5, pady=10, sticky=tk.W)
PhdLnameEntryTabFour.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)


buttonCommit2.grid(row=7, column=0, rowspan=3, padx=15, pady=15)

######################################################################################################################
#Tab5

contents_r = ["Aging", "Behavioural Disorders", "Bioinformatics", "Cancer", "Complex Traits",
            "Computational Biology", "Developmental Biology", "Diabetes", "Fertility",
            "Gene Ontology", "Immune Disorders", "Infectious Disease", "Microbiome",
            "Neurodegenerative Disease", "Neuromuscular Disease", "Neuroscience",
            "Obesity", "Reproductive Disorders", "Resource Development", "Skin Disease",
            "Structural and Regulatory Genomics"]

options_r = tk.StringVar(tab5)
options_r.set("Select Research Focus")

dropdown_r = tk.OptionMenu(tab5, options_r, *contents_r)
buttonSearch = tk.Button(tab5, text="Search", command=display_query_results)


buttonSearch.grid(row=0, column=2, padx=10, pady=10)
dropdown_r.grid(row=0, column=0, padx=10, pady=10)
#######################################################################################################################
############################################################
success = load_database_results()

if success:
    fResearch.set(rows[0][2])
    fPIFname.set(rows[0][0])
    fPILname.set(rows[0][1])
    fCampus.set(rows[0][3])
    photo_path = db_config_file_final_project.PHOTO_DIRECTORY + rows[0][4]
    load_photo_tab_one(photo_path)


tab_parent.pack(expand=1, fill='both')

form.mainloop()