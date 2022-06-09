import datetime
import sqlite3 as sl
import tkinter as tk
from tkinter import Image
from PIL import Image, ImageTk

con = sl.connect('DB/my-test.db')

with con:
    result = con.execute("SELECT * FROM Connection ORDER BY connection_id DESC LIMIT 1")
    for row in result:
        connection_user_id = row[1]

# Dimensijas + mainīgie
HEIGHT = 900
WIDTH = 500

fonts1 = ('Caladea', 17, 'bold')
fonts2 = ('Caladea', 14, 'bold')
fonts3 = ('Caladea', 22, 'bold')

global atverts 
atverts = 0


# GUI sākums
root = tk.Tk()

root.title("Transporta detaļu kontroles rīks ")
root.geometry("+900+100") # vieta, kurā rīks atversies (x un y no ekrāna izmēra)
#       Rīka izmēri
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()


# BackGround picture
image = Image.open("Pictures/backGround.png")
resize_image = image.resize((WIDTH, HEIGHT))
img = ImageTk.PhotoImage(resize_image)
labelBG = tk.Label(image=img)
labelBG.image = img
labelBG.place(relheight=1, relwidth=1)

# Papildus logs 1 
#frame = tk.Frame(root, bg = "#FF9A3D")
#frame.place(relheight=0.5, relwidth=1, relx =0, rely=0.10)


# Odometrs 1


def odometrsLogs():
    global atverts
    if atverts == 0:
        atverts = 1
        frameOdometrs = tk.Label(root, bg = "#FF9A3D")
        frameOdometrs.place(relheight=0.5, relwidth=1, relx =0, rely=0.10)

        odometrsZinojums = tk.Label(root, font=fonts3,justify='center', bg = "#FF9A3D", text="Odometra rādījumu \natjaunināšana:")
        odometrsZinojums.place(relheight=0.2, relwidth=0.7, relx =0.15, rely=0.15)

        with con:
            data = con.execute("SELECT nobraukums FROM Cars WHERE id_user = '%d' AND nosaukums = 'Odometrs' " % connection_user_id)
            for row in data:
                x = row[0]

        odometrsRadijums = tk.IntVar()
        odometrsRadijums.set(x)
        odometrsIevade = tk.Entry(root, font=fonts1, bg='#FFFFFF', textvariable=odometrsRadijums)
        odometrsIevade.place(relheight=0.05, relwidth=0.5, relx=0.25, rely=0.35)

        with con:
            data = con.execute("SELECT datums FROM Cars WHERE id_user = '%d' AND nosaukums = 'Odometrs' " % connection_user_id)
            for row in data:
                y = row[0]
        
        odometrsDatums = tk.Label(root, font=fonts1, bg = "#FF9A3D", text=("Datums - " + y) )
        odometrsDatums.place(relheight=0.05, relwidth=0.5, relx=0.25, rely=0.4)

        buttonOdometrsAizver = tk.Button(root, text="Atcelt", font=fonts1, bg = "#FF9A3D", command = lambda: odometrsLogsAizvert())
        buttonOdometrsAizver.place(relheight=0.05, relwidth=0.3, relx=0.35, rely=0.55)
        buttonOdometrsSaglabat = tk.Button(root, text="Apstiprināt", font=fonts1, bg = "#FF9A3D", command = lambda: odometrsLogsSaglbat())
        buttonOdometrsSaglabat.place(relheight=0.05, relwidth=0.3, relx=0.35, rely=0.5)

        def odometrsLogsAizvert():
            global atverts
            odometrsDatums.destroy()
            odometrsIevade.destroy()
            odometrsZinojums.destroy()
            buttonOdometrsSaglabat.destroy()
            buttonOdometrsAizver.destroy()
            frameOdometrs.destroy()
            atverts = 0
        def odometrsLogsSaglbat():
            global atverts
            nobraukums = odometrsRadijums.get()

            sql = str("UPDATE Cars SET nobraukums='"+str(nobraukums)+ "'  WHERE id_user = '%d' AND nosaukums = 'Odometrs'" % connection_user_id)
            con.execute(sql)
            con.commit()


            dateTd = datetime.datetime.today().strftime('%Y-%m-%d')
            dateTd = str(dateTd)

            sql = str("UPDATE Cars SET datums='"+ dateTd + "'  WHERE id_user = '%d' AND nosaukums = 'Odometrs'" % connection_user_id)
            con.execute(sql)
            con.commit()

            parbaudeKM()
            odometrsLogsAizvert()
            print("Saglabāts DB")
            atverts = 0


virsraksts1 = tk.Label(root, text="Nobraukums:", justify='center',  font=fonts1, bg='#FFFFFF')
virsraksts1.place( relx=0.35, rely=0.18)

image2 = Image.open("Pictures/aCmwIm9bEIS1.png")
resize_image2 = image2.resize((50, 50))
img2 = ImageTk.PhotoImage(resize_image2)
button1 = tk.Button(image=img2, command = lambda: odometrsLogs())
button1.place( relx=0.85, rely=0.24)

virsraksts1_1 = tk.Label(root, text="234681 km", justify='center',  font=fonts2, bg='#FFFFFF',borderwidth=2,relief="solid")
virsraksts1_1.place( relx=0.05, rely=0.25, relheight=0.05, relwidth=0.35)
virsraksts1_2 = tk.Label(root, text="23/02/2022", justify='center',  font=fonts2, bg='#FFFFFF',borderwidth=2,relief="solid")
virsraksts1_2.place( relx=0.45, rely=0.25, relheight=0.05, relwidth=0.35)




# Dzineja eļļa

def ellaLogs():
    frameElla = tk.Label(root, bg = "#FF9A3D")
    frameElla.place(relheight=0.5, relwidth=1, relx =0, rely=0.10)

    ellaZinojums = tk.Label(root, font=fonts3,justify='center', bg = "#FF9A3D", text="Eļļas maiņās rādījumu \natjaunināšana:")
    ellaZinojums.place(relheight=0.2, relwidth=0.7, relx =0.15, rely=0.15)

    with con:
        data = con.execute("SELECT nobraukums FROM Cars WHERE id_user = '%d' AND nosaukums = 'Ella' " % connection_user_id)
        for row in data:
            x = row[0]

    ellaRadijums = tk.IntVar()
    ellaRadijums.set(x)
    ellaIevade = tk.Entry(root, font=fonts1, bg='#FFFFFF', textvariable=ellaRadijums)
    ellaIevade.place(relheight=0.05, relwidth=0.5, relx=0.25, rely=0.35)

    

    with con:
        data = con.execute("SELECT datums FROM Cars WHERE id_user = '%d' AND nosaukums = 'Ella' " % connection_user_id)
        for row in data:
            y = row[0]

    ellaDatums = tk.Label(root, font=fonts1, bg = "#FF9A3D", text=("Datums - " + y)  )
    ellaDatums.place(relheight=0.05, relwidth=0.5, relx=0.25, rely=0.4)


    buttonellaAizver = tk.Button(root, text="Atcelt", font=fonts1, bg = "#FF9A3D", command = lambda: ellaLogsAizvert())
    buttonellaAizver.place(relheight=0.05, relwidth=0.3, relx=0.35, rely=0.55)
    buttonellaSaglabat = tk.Button(root, text="Apstiprināt", font=fonts1, bg = "#FF9A3D", command = lambda: ellaLogsSaglbat())
    buttonellaSaglabat.place(relheight=0.05, relwidth=0.3, relx=0.35, rely=0.5)

    def ellaLogsAizvert():
        ellaDatums.destroy()
        ellaIevade.destroy()
        ellaZinojums.destroy()
        buttonellaSaglabat.destroy()
        buttonellaAizver.destroy()
        frameElla.destroy()
    def ellaLogsSaglbat():

        nobraukums = ellaRadijums.get()


        sql = str("UPDATE Cars SET nobraukums='"+str(nobraukums)+ "'  WHERE id_user = '%d' AND nosaukums = 'Ella'" % connection_user_id)
        con.execute(sql)
        con.commit()

        dateTd = datetime.datetime.today().strftime('%Y-%m-%d')
        dateTd = str(dateTd)

        sql = str("UPDATE Cars SET datums='"+ dateTd + "'  WHERE id_user = '%d' AND nosaukums = 'Ella'" % connection_user_id)
        con.execute(sql)
        con.commit()


        parbaudeKM()
        ellaLogsAizvert()
        print("Saglabāts DB")


virsraksts2 = tk.Label(root, text="Dzinēja eļļas un filtra maiņā veikta:", justify='center',  font=fonts1, bg='#FFFFFF')
virsraksts2.place( relx=0.05, rely=0.34)

image3 = Image.open("Pictures/aCmwIm9bEIS1.png")
resize_image3 = image3.resize((50, 50))
img3 = ImageTk.PhotoImage(resize_image3)
button2 = tk.Button(image=img3, command = lambda: ellaLogs())
button2.place( relx=0.85, rely=0.37)

virsraksts2_1 = tk.Label(root, text="239681 km", justify='center',  font=fonts2, bg='#FFFFFF',borderwidth=2,relief="solid")
virsraksts2_1.place( relx=0.05, rely=0.38, relheight=0.05, relwidth=0.35)
virsraksts2_2 = tk.Label(root, text="23/02/2022", justify='center',  font=fonts2, bg='#FFFFFF',borderwidth=2,relief="solid")
virsraksts2_2.place( relx=0.45, rely=0.38, relheight=0.05, relwidth=0.35)



# Gaisa filtru maiņa veikta


def filtriLogs():
    global atverts
    if atverts == 0:
        atverts = 1
        framefiltri = tk.Label(root, bg = "#FF9A3D")
        framefiltri.place(relheight=0.5, relwidth=1, relx =0, rely=0.10)

        filtriZinojums = tk.Label(root, font=fonts3,justify='center', bg = "#FF9A3D", text="Filtru maiņās rādījumu \natjaunināšana:")
        filtriZinojums.place(relheight=0.2, relwidth=0.7, relx =0.15, rely=0.15)

        with con:
            data = con.execute("SELECT nobraukums FROM Cars WHERE id_user = '%d' AND nosaukums = 'Filtri' " % connection_user_id)
            for row in data:
                x = row[0]

        filtriRadijums = tk.IntVar()
        filtriRadijums.set(x)
        filtriIevade = tk.Entry(root, font=fonts1, bg='#FFFFFF', textvariable=filtriRadijums)
        filtriIevade.place(relheight=0.05, relwidth=0.5, relx=0.25, rely=0.35)
      
        with con:
            data = con.execute("SELECT datums FROM Cars WHERE id_user = '%d' AND nosaukums = 'Filtri' " % connection_user_id)
            for row in data:
                y = row[0]

  
        filtriDatums = tk.Label(root, font=fonts1, bg = "#FF9A3D", text=("Datums - " + y))
        filtriDatums.place(relheight=0.05, relwidth=0.5, relx=0.25, rely=0.4)

        buttonfiltriAizver = tk.Button(root, text="Atcelt", font=fonts1, bg = "#FF9A3D", command = lambda: filtriLogsAizvert())
        buttonfiltriAizver.place(relheight=0.05, relwidth=0.3, relx=0.35, rely=0.55)
        buttonfiltriSaglabat = tk.Button(root, text="Apstiprināt", font=fonts1, bg = "#FF9A3D", command = lambda: filtriLogsSaglbat())
        buttonfiltriSaglabat.place(relheight=0.05, relwidth=0.3, relx=0.35, rely=0.5)

        def filtriLogsAizvert():
            global atverts 
            atverts = 0
            filtriDatums.destroy()
            filtriIevade.destroy()
            filtriZinojums.destroy()
            buttonfiltriSaglabat.destroy()
            buttonfiltriAizver.destroy()
            framefiltri.destroy()
        def filtriLogsSaglbat():
            global atverts 
            atverts = 0

            nobraukums = filtriRadijums.get()
            sql = str("UPDATE Cars SET nobraukums='"+str(nobraukums)+ "'  WHERE id_user = '%d' AND nosaukums = 'Filtri'" % connection_user_id)
            con.execute(sql)
            con.commit()

            dateTd = datetime.datetime.today().strftime('%Y-%m-%d')
            dateTd = str(dateTd)

            sql = str("UPDATE Cars SET datums='"+ dateTd + "'  WHERE id_user = '%d' AND nosaukums = 'Filtri'" % connection_user_id)
            con.execute(sql)
            con.commit()

            parbaudeKM()
            filtriLogsAizvert()
            print("Saglabāts DB")


virsraksts3 = tk.Label(root, text="Gaisa filtru maiņa veikta:", justify='center',  font=fonts1, bg='#FFFFFF')
virsraksts3.place( relx=0.05, rely=0.48)

image4 = Image.open("Pictures/aCmwIm9bEIS1.png")
resize_image4 = image4.resize((50, 50))
img4 = ImageTk.PhotoImage(resize_image4)
button3 = tk.Button(image=img4, command = lambda: filtriLogs())
button3.place( relx=0.85, rely=0.51)

virsraksts3_1 = tk.Label(root, text="229681 km", justify='center',  font=fonts2, bg='#FFFFFF',borderwidth=2,relief="solid")
virsraksts3_1.place( relx=0.05, rely=0.52, relheight=0.05, relwidth=0.35)
virsraksts3_2 = tk.Label(root, text="23/02/2022", justify='center',  font=fonts2, bg='#FFFFFF',borderwidth=2,relief="solid")
virsraksts3_2.place( relx=0.45, rely=0.52, relheight=0.05, relwidth=0.35)




# Bremžu suporti

def suportiLogs():
    global atverts
    if atverts == 0:
        atverts = 1
        frameSuporti = tk.Label(root, bg = "#FF9A3D")
        frameSuporti.place(relheight=0.5, relwidth=1, relx =0, rely=0.10)

        SuportiZinojums = tk.Label(root, font=fonts3,justify='center', bg = "#FF9A3D", text="Bremžu suportu \nmaiņās rādījumu \natjaunināšana:")
        SuportiZinojums.place(relheight=0.2, relwidth=0.7, relx =0.15, rely=0.15)

        with con:
            data = con.execute("SELECT nobraukums FROM Cars WHERE id_user = '%d' AND nosaukums = 'Suporti' " % connection_user_id)
            for row in data:
                x = row[0]

        SuportiRadijums = tk.IntVar()
        SuportiRadijums.set(x)
        SuportiIevade = tk.Entry(root, font=fonts1, bg='#FFFFFF', textvariable=SuportiRadijums)
        SuportiIevade.place(relheight=0.05, relwidth=0.5, relx=0.25, rely=0.35)


        with con:
            data = con.execute("SELECT datums FROM Cars WHERE id_user = '%d' AND nosaukums = 'Suporti' " % connection_user_id)
            for row in data:
                y = row[0]
        
        SuportiDatums = tk.Label(root, font=fonts1, bg = "#FF9A3D", text=("Datums - " + y))
        SuportiDatums.place(relheight=0.05, relwidth=0.5, relx=0.25, rely=0.4)

        buttonSuportiAizver = tk.Button(root, text="Atcelt", font=fonts1, bg = "#FF9A3D", command = lambda: SuportiLogsAizvert())
        buttonSuportiAizver.place(relheight=0.05, relwidth=0.3, relx=0.35, rely=0.55)
        buttonSuportiSaglabat = tk.Button(root, text="Apstiprināt", font=fonts1, bg = "#FF9A3D", command = lambda: SuportiLogsSaglbat())
        buttonSuportiSaglabat.place(relheight=0.05, relwidth=0.3, relx=0.35, rely=0.5)

        def SuportiLogsAizvert():
            global atverts
            atverts = 0
            SuportiDatums.destroy()
            SuportiIevade.destroy()
            SuportiZinojums.destroy()
            buttonSuportiSaglabat.destroy()
            buttonSuportiAizver.destroy()
            frameSuporti.destroy()
        def SuportiLogsSaglbat():
            global atverts
            atverts = 0

            nobraukums = SuportiRadijums.get()
            sql = str("UPDATE Cars SET nobraukums='"+str(nobraukums)+ "'  WHERE id_user = '%d' AND nosaukums = 'Suporti'" % connection_user_id)
            con.execute(sql)
            con.commit()

            dateTd = datetime.datetime.today().strftime('%Y-%m-%d')
            dateTd = str(dateTd)

            sql = str("UPDATE Cars SET datums='"+ dateTd + "'  WHERE id_user = '%d' AND nosaukums = 'Suporti'" % connection_user_id)
            con.execute(sql)
            con.commit()


            parbaudeKM()
            SuportiLogsAizvert()
            print("Saglabāts DB")


virsraksts4 = tk.Label(root, text="Bremžu suportu maiņa veikta:", justify='center',  font=fonts1, bg='#FFFFFF')
virsraksts4.place( relx=0.05, rely=0.62)

image5 = Image.open("Pictures/aCmwIm9bEIS1.png")
resize_image5 = image5.resize((50, 50))
img5 = ImageTk.PhotoImage(resize_image5)
button4 = tk.Button(image=img5, command = lambda: suportiLogs())
button4.place( relx=0.85, rely=0.65)

virsraksts4_1 = tk.Label(root, text="226681 km", justify='center',  font=fonts2, bg='#FFFFFF',borderwidth=2,relief="solid")
virsraksts4_1.place( relx=0.05, rely=0.66, relheight=0.05, relwidth=0.35)
virsraksts4_2 = tk.Label(root, text="23/02/2022", justify='center',  font=fonts2, bg='#FFFFFF',borderwidth=2,relief="solid")
virsraksts4_2.place( relx=0.45, rely=0.66, relheight=0.05, relwidth=0.35)



# Bremžu kluči

def kluciLogs():
    global atverts
    if atverts == 0:
        atverts = 1
        frameKluci = tk.Label(root, bg = "#FF9A3D")
        frameKluci.place(relheight=0.5, relwidth=1, relx =0, rely=0.10)

        KluciZinojums = tk.Label(root, font=fonts3,justify='center', bg = "#FF9A3D", text="Bremžu kluču \nmaiņās rādījumu \natjaunināšana:")
        KluciZinojums.place(relheight=0.2, relwidth=0.7, relx =0.15, rely=0.15)

        with con:
            data = con.execute("SELECT nobraukums FROM Cars WHERE id_user = '%d' AND nosaukums = 'Kluci' " % connection_user_id)
            for row in data:
                x = row[0]

        KluciRadijums = tk.IntVar()
        KluciRadijums.set(x)
        KluciIevade = tk.Entry(root, font=fonts1, bg='#FFFFFF', textvariable=KluciRadijums)
        KluciIevade.place(relheight=0.05, relwidth=0.5, relx=0.25, rely=0.35)

        with con:
            data = con.execute("SELECT datums FROM Cars WHERE id_user = '%d' AND nosaukums = 'Kluci' " % connection_user_id)
            for row in data:
                y = row[0]
        
        KluciDatums = tk.Label(root, font=fonts1, bg = "#FF9A3D", text=("Datums - " + y))
        KluciDatums.place(relheight=0.05, relwidth=0.5, relx=0.25, rely=0.4)

        buttonKluciAizver = tk.Button(root, text="Atcelt", font=fonts1, bg = "#FF9A3D", command = lambda: KluciLogsAizvert())
        buttonKluciAizver.place(relheight=0.05, relwidth=0.3, relx=0.35, rely=0.55)
        buttonKluciSaglabat = tk.Button(root, text="Apstiprināt", font=fonts1, bg = "#FF9A3D", command = lambda: KluciLogsSaglbat())
        buttonKluciSaglabat.place(relheight=0.05, relwidth=0.3, relx=0.35, rely=0.5)

        def KluciLogsAizvert():
            global atverts
            atverts = 0

            KluciDatums.destroy()
            KluciIevade.destroy()
            KluciZinojums.destroy()
            buttonKluciSaglabat.destroy()
            buttonKluciAizver.destroy()
            frameKluci.destroy()
        def KluciLogsSaglbat():
            global atverts
            atverts = 0

            nobraukums = KluciRadijums.get()
            sql = str("UPDATE Cars SET nobraukums='"+str(nobraukums)+ "'  WHERE id_user = '%d' AND nosaukums = 'Kluci'" % connection_user_id)
            con.execute(sql)
            con.commit()

            dateTd = datetime.datetime.today().strftime('%Y-%m-%d')
            dateTd = str(dateTd)

            sql = str("UPDATE Cars SET datums='"+ dateTd + "'  WHERE id_user = '%d' AND nosaukums = 'Kluci'" % connection_user_id)
            con.execute(sql)
            con.commit()

            parbaudeKM()
            KluciLogsAizvert()
            print("Saglabāts DB")
        
virsraksts5 = tk.Label(root, text="Bremžu kluču maiņa veikta:", justify='center',  font=fonts1, bg='#FFFFFF')
virsraksts5.place( relx=0.05, rely=0.76)

image6 = Image.open("Pictures/aCmwIm9bEIS1.png")
resize_image6 = image6.resize((50, 50))
img6 = ImageTk.PhotoImage(resize_image6)
button6 = tk.Button(image=img6, command = lambda: kluciLogs())
button6.place( relx=0.85, rely=0.79)

virsraksts5_1 = tk.Label(root, text="229991 km", justify='center',  font=fonts2, bg='#FFFFFF',borderwidth=2,relief="solid")
virsraksts5_1.place( relx=0.05, rely=0.8, relheight=0.05, relwidth=0.35)
virsraksts5_2 = tk.Label(root, text="23/02/2022", justify='center',  font=fonts2, bg='#FFFFFF',borderwidth=2,relief="solid")
virsraksts5_2.place( relx=0.45, rely=0.8, relheight=0.05, relwidth=0.35)


# Bremžu šķidrums

def skidrumsLogs():
    global atverts
    if atverts == 0:
        atverts = 1
        frameSkidrums = tk.Label(root, bg = "#FF9A3D")
        frameSkidrums.place(relheight=0.5, relwidth=1, relx =0, rely=0.10)

        SkidrumsZinojums = tk.Label(root, font=fonts3,justify='center', bg = "#FF9A3D", text="Bremžu šķidruma \nmaiņās rādījumu \natjaunināšana:")
        SkidrumsZinojums.place(relheight=0.2, relwidth=0.7, relx =0.15, rely=0.15)

        with con:
            data = con.execute("SELECT nobraukums FROM Cars WHERE id_user = '%d' AND nosaukums = 'Skidrums' " % connection_user_id)
            for row in data:
                x = row[0]

        SkidrumsRadijums = tk.IntVar()
        SkidrumsRadijums.set(x)

        SkidrumsIevade = tk.Entry(root, font=fonts1, bg='#FFFFFF', textvariable=SkidrumsRadijums)
        SkidrumsIevade.place(relheight=0.05, relwidth=0.5, relx=0.25, rely=0.35)

        with con:
            data = con.execute("SELECT datums FROM Cars WHERE id_user = '%d' AND nosaukums = 'Skidrums' " % connection_user_id)
            for row in data:
                y = row[0]

        SkidrumsDatums = tk.Label(root, font=fonts1, bg = "#FF9A3D", text=("Datums - " + y))
        SkidrumsDatums.place(relheight=0.05, relwidth=0.5, relx=0.25, rely=0.4)

        buttonSkidrumsAizver = tk.Button(root, text="Atcelt", font=fonts1, bg = "#FF9A3D", command = lambda: SkidrumsLogsAizvert())
        buttonSkidrumsAizver.place(relheight=0.05, relwidth=0.3, relx=0.35, rely=0.55)
        buttonSkidrumsSaglabat = tk.Button(root, text="Apstiprināt", font=fonts1, bg = "#FF9A3D", command = lambda: SkidrumsLogsSaglbat())
        buttonSkidrumsSaglabat.place(relheight=0.05, relwidth=0.3, relx=0.35, rely=0.5)

        def SkidrumsLogsAizvert():
            global atverts
            atverts = 0
            SkidrumsDatums.destroy()
            SkidrumsIevade.destroy()
            SkidrumsZinojums.destroy()
            buttonSkidrumsSaglabat.destroy()
            buttonSkidrumsAizver.destroy()
            frameSkidrums.destroy()
        def SkidrumsLogsSaglbat():
            global atverts
            atverts = 0

            nobraukums = SkidrumsRadijums.get()
            sql = str("UPDATE Cars SET nobraukums='"+str(nobraukums)+ "'  WHERE id_user = '%d' AND nosaukums = 'Skidrums'" % connection_user_id)
            con.execute(sql)
            con.commit()

            dateTd = datetime.datetime.today().strftime('%Y-%m-%d')
            dateTd = str(dateTd)

            sql = str("UPDATE Cars SET datums='"+ dateTd + "'  WHERE id_user = '%d' AND nosaukums = 'Skidrums'" % connection_user_id)
            con.execute(sql)
            con.commit()

            parbaudeKM()
            SkidrumsLogsAizvert()
            print("Saglabāts DB")

virsraksts6 = tk.Label(root, text="Bremžu šķidruma maiņa veikta:", justify='center',  font=fonts1, bg='#FFFFFF')
virsraksts6.place( relx=0.05, rely=0.89)

image7 = Image.open("Pictures/aCmwIm9bEIS1.png")
resize_image7 = image7.resize((50, 50))
img7 = ImageTk.PhotoImage(resize_image7)
button7 = tk.Button(image=img7, command = lambda: skidrumsLogs())
button7.place( relx=0.85, rely=0.92)

virsraksts6_1 = tk.Label(root, text="224681 km", justify='center',  font=fonts2, bg='#FFFFFF',borderwidth=2,relief="solid")
virsraksts6_1.place( relx=0.05, rely=0.93, relheight=0.05, relwidth=0.35)
virsraksts6_2 = tk.Label(root, text="23/02/2022", justify='center',  font=fonts2, bg='#FFFFFF',borderwidth=2,relief="solid")
virsraksts6_2.place( relx=0.45, rely=0.93, relheight=0.05, relwidth=0.35)



with con:
    data = con.execute("SELECT nobraukums FROM Cars WHERE id_user = '%d' AND nosaukums = 'Odometrs' " % connection_user_id)
    for row in data:
        print(row[0])


#       Parbaude:
def parbaudeKM():

    #   Datu bāze:
    con = sl.connect('DB/my-test.db')

    with con:
        data = con.execute("SELECT * FROM Cars WHERE id_user = '%d'" % connection_user_id)
        for row in data:
            i = row
            print(row)
            if i[1] == 'Odometrs':
                virsraksts1_1.config(text=str(str(i[2]) + " km"))
                virsraksts1_2.config(text=str(str(i[3])))
            if i[1] == 'Ella':
                virsraksts2_1.config(text=str(str(i[2]) + " km"))
                virsraksts2_2.config(text=str(str(i[3])))
            if i[1] == 'Filtri':
                virsraksts3_1.config(text=str(str(i[2]) + " km"))
                virsraksts3_2.config(text=str(str(i[3])))
            if i[1] == 'Suporti':
                virsraksts4_1.config(text=str(str(i[2]) + " km"))
                virsraksts4_2.config(text=str(str(i[3])))
            if i[1] == 'Kluci':
                virsraksts5_1.config(text=str(str(i[2]) + " km"))
                virsraksts5_2.config(text=str(str(i[3])))
            if i[1] == 'Skidrums':
                virsraksts6_1.config(text=str(str(i[2]) + " km"))
                virsraksts6_2.config(text=str(str(i[3])))


    # Odometrs
    odometrsKm = virsraksts1_1['text']
    odometrsKm=odometrsKm[:-3]
    odometrsKm=int(odometrsKm)


    timeToday = datetime.datetime.today().strftime('%Y-%m-%d')
    timeToday = datetime.datetime.strptime(timeToday, "%Y-%m-%d") # .strftime("%Y-%m-%d")
    odometrsDatums = virsraksts1_2['text']
    odometrsDatums = datetime.datetime.strptime(odometrsDatums, "%Y-%m-%d") # .strftime("%Y-%m-%d")
   

    # Eļļa
    ellaKm = virsraksts2_1['text']
    ellaKm=ellaKm[:-3]
    ellaKm=int(ellaKm)

    
    if odometrsKm - ellaKm > 9000:
        virsraksts2_1.config(bg = "#eb3434")
    elif odometrsKm - ellaKm > 8000:
        virsraksts2_1.config(bg = "#c44b35")
    elif odometrsKm - ellaKm > 6000:
        virsraksts2_1.config(bg = "#eb6534")
    elif odometrsKm - ellaKm > 5000:
        virsraksts2_1.config(bg = "#eba834")
    elif odometrsKm - ellaKm > 4000:
        virsraksts2_1.config(bg = "#a8eb34")
    elif odometrsKm - ellaKm > 3000:
        virsraksts2_1.config(bg = "#d3eb34")
    elif odometrsKm - ellaKm > 2000:
        virsraksts2_1.config(bg = "#89eb34")
    elif odometrsKm - ellaKm > 1000:
        virsraksts2_1.config(bg = "#7aeb34")
    else:
        virsraksts2_1.config(bg = "#59eb34")   


    ellaDatums = virsraksts2_2['text']
    ellaDatums = datetime.datetime.strptime(ellaDatums, "%Y-%m-%d") # .strftime("%Y-%m-%d")


    if odometrsDatums - ellaDatums > datetime.timedelta(days= 365):
        virsraksts2_2.config(bg = "#eb3434")
    elif odometrsDatums - ellaDatums > datetime.timedelta(days= 325):
        virsraksts2_2.config(bg = "#c44b35")
    elif odometrsDatums - ellaDatums > datetime.timedelta(days= 285):
        virsraksts2_2.config(bg = "#eb6534")
    elif odometrsDatums - ellaDatums > datetime.timedelta(days= 245):
        virsraksts2_2.config(bg = "#eba834")
    elif odometrsDatums - ellaDatums > datetime.timedelta(days= 205):
        virsraksts2_2.config(bg = "#a8eb34")
    elif odometrsDatums - ellaDatums > datetime.timedelta(days= 165):
        virsraksts2_2.config(bg = "#d3eb34")
    elif odometrsDatums - ellaDatums > datetime.timedelta(days= 125):
        virsraksts2_2.config(bg = "#89eb34")
    elif odometrsDatums - ellaDatums > datetime.timedelta(days= 85):
        virsraksts2_2.config(bg = "#7aeb34")
    else:
        virsraksts2_2.config(bg = "#59eb34")   


    # Gaisa filtri
    filtriKm = virsraksts3_1['text']
    filtriKm=filtriKm[:-3]
    filtriKm=int(filtriKm)

    if odometrsKm - filtriKm > 9000:
        virsraksts3_1.config(bg = "#eb3434")
    elif odometrsKm - filtriKm > 8000:
        virsraksts3_1.config(bg = "#c44b35")
    elif odometrsKm - filtriKm > 6000:
        virsraksts3_1.config(bg = "#eb6534")
    elif odometrsKm - filtriKm > 5000:
        virsraksts3_1.config(bg = "#eba834")
    elif odometrsKm - filtriKm > 4000:
        virsraksts3_1.config(bg = "#a8eb34")
    elif odometrsKm - filtriKm > 3000:
        virsraksts3_1.config(bg = "#d3eb34")
    elif odometrsKm - filtriKm > 2000:
        virsraksts3_1.config(bg = "#89eb34")
    elif odometrsKm - filtriKm > 1000:
        virsraksts3_1.config(bg = "#7aeb34")
    else:
        virsraksts3_1.config(bg = "#59eb34")  


    filtriDatums = virsraksts3_2['text']
    filtriDatums = datetime.datetime.strptime(filtriDatums, "%Y-%m-%d") # .strftime("%Y-%m-%d")


    if odometrsDatums - filtriDatums > datetime.timedelta(days= 365):
        virsraksts3_2.config(bg = "#eb3434")
    elif odometrsDatums - filtriDatums > datetime.timedelta(days= 325):
        virsraksts3_2.config(bg = "#c44b35")
    elif odometrsDatums - filtriDatums > datetime.timedelta(days= 285):
        virsraksts3_2.config(bg = "#eb6534")
    elif odometrsDatums - filtriDatums > datetime.timedelta(days= 245):
        virsraksts3_2.config(bg = "#eba834")
    elif odometrsDatums - filtriDatums > datetime.timedelta(days= 205):
        virsraksts3_2.config(bg = "#a8eb34")
    elif odometrsDatums - filtriDatums > datetime.timedelta(days= 165):
        virsraksts3_2.config(bg = "#d3eb34")
    elif odometrsDatums - filtriDatums > datetime.timedelta(days= 125):
        virsraksts3_2.config(bg = "#89eb34")
    elif odometrsDatums - filtriDatums > datetime.timedelta(days= 85):
        virsraksts3_2.config(bg = "#7aeb34")
    else:
        virsraksts3_2.config(bg = "#59eb34")   


    # Bremžu suporti
    suportiKm = virsraksts4_1['text']
    suportiKm=suportiKm[:-3]
    suportiKm=int(suportiKm)

    if odometrsKm - suportiKm > 9000:
        virsraksts4_1.config(bg = "#eb3434")
    elif odometrsKm - suportiKm > 8000:
        virsraksts4_1.config(bg = "#c44b35")
    elif odometrsKm - suportiKm > 6000:
        virsraksts4_1.config(bg = "#eb6534")
    elif odometrsKm - suportiKm > 5000:
        virsraksts4_1.config(bg = "#eba834")
    elif odometrsKm - suportiKm > 4000:
        virsraksts4_1.config(bg = "#a8eb34")
    elif odometrsKm - suportiKm > 3000:
        virsraksts4_1.config(bg = "#d3eb34")
    elif odometrsKm - suportiKm > 2000:
        virsraksts4_1.config(bg = "#89eb34")
    elif odometrsKm - suportiKm > 1000:
        virsraksts4_1.config(bg = "#7aeb34")
    else:
        virsraksts4_1.config(bg = "#59eb34")  


    suportiDatums = virsraksts4_2['text']
    suportiDatums = datetime.datetime.strptime(suportiDatums, "%Y-%m-%d") # .strftime("%Y-%m-%d")


    if odometrsDatums - suportiDatums > datetime.timedelta(days= 365):
        virsraksts4_2.config(bg = "#eb3434")
    elif odometrsDatums - suportiDatums > datetime.timedelta(days= 325):
        virsraksts4_2.config(bg = "#c44b35")
    elif odometrsDatums - suportiDatums > datetime.timedelta(days= 285):
        virsraksts4_2.config(bg = "#eb6534")
    elif odometrsDatums - suportiDatums > datetime.timedelta(days= 245):
        virsraksts4_2.config(bg = "#eba834")
    elif odometrsDatums - suportiDatums > datetime.timedelta(days= 205):
        virsraksts4_2.config(bg = "#a8eb34")
    elif odometrsDatums - suportiDatums > datetime.timedelta(days= 165):
        virsraksts4_2.config(bg = "#d3eb34")
    elif odometrsDatums - suportiDatums > datetime.timedelta(days= 125):
        virsraksts4_2.config(bg = "#89eb34")
    elif odometrsDatums - suportiDatums > datetime.timedelta(days= 85):
        virsraksts4_2.config(bg = "#7aeb34")
    else:
        virsraksts4_2.config(bg = "#59eb34")   


    # Bremžu kluči
    kluciKm = virsraksts5_1['text']
    kluciKm=kluciKm[:-3]
    kluciKm=int(kluciKm)

    if odometrsKm - kluciKm > 9000:
        virsraksts5_1.config(bg = "#eb3434")
    elif odometrsKm - kluciKm > 8000:
        virsraksts5_1.config(bg = "#c44b35")
    elif odometrsKm - kluciKm > 6000:
        virsraksts5_1.config(bg = "#eb6534")
    elif odometrsKm - kluciKm > 5000:
        virsraksts5_1.config(bg = "#eba834")
    elif odometrsKm - kluciKm > 4000:
        virsraksts5_1.config(bg = "#a8eb34")
    elif odometrsKm - kluciKm > 3000:
        virsraksts5_1.config(bg = "#d3eb34")
    elif odometrsKm - kluciKm > 2000:
        virsraksts5_1.config(bg = "#89eb34")
    elif odometrsKm - kluciKm > 1000:
        virsraksts5_1.config(bg = "#7aeb34")
    else:
        virsraksts5_1.config(bg = "#59eb34")  


    kluciDatums = virsraksts5_2['text']
    kluciDatums = datetime.datetime.strptime(kluciDatums, "%Y-%m-%d") # .strftime("%Y-%m-%d")


    if odometrsDatums - kluciDatums > datetime.timedelta(days= 365):
        virsraksts5_2.config(bg = "#eb3434")
    elif odometrsDatums - kluciDatums > datetime.timedelta(days= 325):
        virsraksts5_2.config(bg = "#c44b35")
    elif odometrsDatums - kluciDatums > datetime.timedelta(days= 285):
        virsraksts5_2.config(bg = "#eb6534")
    elif odometrsDatums - kluciDatums > datetime.timedelta(days= 245):
        virsraksts5_2.config(bg = "#eba834")
    elif odometrsDatums - kluciDatums > datetime.timedelta(days= 205):
        virsraksts5_2.config(bg = "#a8eb34")
    elif odometrsDatums - kluciDatums > datetime.timedelta(days= 165):
        virsraksts5_2.config(bg = "#d3eb34")
    elif odometrsDatums - kluciDatums > datetime.timedelta(days= 125):
        virsraksts5_2.config(bg = "#89eb34")
    elif odometrsDatums - kluciDatums > datetime.timedelta(days= 85):
        virsraksts5_2.config(bg = "#7aeb34")
    else:
        virsraksts5_2.config(bg = "#59eb34")   


    # Bremžu šķidrums
    skidrumsKm = virsraksts6_1['text']
    skidrumsKm=skidrumsKm[:-3]
    skidrumsKm=int(skidrumsKm)

    if odometrsKm - skidrumsKm > 9000:
        virsraksts6_1.config(bg = "#eb3434")
    elif odometrsKm - skidrumsKm > 8000:
        virsraksts6_1.config(bg = "#c44b35")
    elif odometrsKm - skidrumsKm > 6000:
        virsraksts6_1.config(bg = "#eb6534")
    elif odometrsKm - skidrumsKm > 5000:
        virsraksts6_1.config(bg = "#eba834")
    elif odometrsKm - skidrumsKm > 4000:
        virsraksts6_1.config(bg = "#a8eb34")
    elif odometrsKm - skidrumsKm > 3000:
        virsraksts6_1.config(bg = "#d3eb34")
    elif odometrsKm - skidrumsKm > 2000:
        virsraksts6_1.config(bg = "#89eb34")
    elif odometrsKm - skidrumsKm > 1000:
        virsraksts6_1.config(bg = "#7aeb34")
    else:
        virsraksts6_1.config(bg = "#59eb34")  



    skidrumsDatums = virsraksts6_2['text']
    skidrumsDatums = datetime.datetime.strptime(skidrumsDatums, "%Y-%m-%d") # .strftime("%Y-%m-%d")


    if odometrsDatums - skidrumsDatums > datetime.timedelta(days= 365):
        virsraksts6_2.config(bg = "#eb3434")
    elif odometrsDatums - skidrumsDatums > datetime.timedelta(days= 325):
        virsraksts6_2.config(bg = "#c44b35")
    elif odometrsDatums - skidrumsDatums > datetime.timedelta(days= 285):
        virsraksts6_2.config(bg = "#eb6534")
    elif odometrsDatums - skidrumsDatums > datetime.timedelta(days= 245):
        virsraksts6_2.config(bg = "#eba834")
    elif odometrsDatums - skidrumsDatums > datetime.timedelta(days= 205):
        virsraksts6_2.config(bg = "#a8eb34")
    elif odometrsDatums - skidrumsDatums > datetime.timedelta(days= 165):
        virsraksts6_2.config(bg = "#d3eb34")
    elif odometrsDatums - skidrumsDatums > datetime.timedelta(days= 125):
        virsraksts6_2.config(bg = "#89eb34")
    elif odometrsDatums - skidrumsDatums > datetime.timedelta(days= 85):
        virsraksts6_2.config(bg = "#7aeb34")
    else:
        virsraksts6_2.config(bg = "#59eb34")   

if __name__ == "__main__":
    parbaudeKM()
    # GUI beigas
    root.mainloop()
