import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import snap7
import ttkbootstrap as ttk
import mysql.connector

# Function to connect to the PLC
def connect_plc():
    ip_address = ip_entry.get()
    plc = snap7.client.Client()
    try:
        plc.connect(ip_address, 0, 1)
        messagebox.showinfo("Success", "Connected to PLC")
       
    except snap7.snap7exceptions.Snap7Exception as e:
        messagebox.showerror("Error", str(e))

# Function to read data from the PLC
def read_data():
    ip_address = ip_entry.get()
    plc = snap7.client.Client()
    plc.connect(ip_address, 0, 1)

    db_number = int(dbR_spinbox.get())
    byte_number = int (byteR_spinbox.get())
    a = db_number
    b= byte_number
    
    if plc.get_connected():
      data = plc.db_read(a, 0, 6)
      var1= snap7.util.get_int(data,b)
      read_label.config(text="" + str(var1))

    print(' Value: ' + str(var1))

    plc.disconnect()



# Function to write data to the PLC
def write_data():
    ip_address = ip_entry.get()
    plc = snap7.client.Client()
    plc.connect(ip_address, 0, 1)


    db_number = int(db_spinbox.get())
    byte_number = int (byte_spinbox.get())
    value = int(value_entry.get())

  
    if plc.get_connected():
      data = plc.db_read(db_number, 0, 6)
      snap7.util.set_int(data,byte_number,value)
      plc.db_write(db_number, 0, data)
    plc.disconnect()


# Function to write OUTPUTS to the PLC
def writeBool():
    ip_address = ip_entry.get()
    plc = snap7.client.Client()
    plc.connect(ip_address, 0, 1)
    

    reading = plc.db_read(2, 0, 1)    
    snap7.util.set_bool(reading, 0, 0, switches[0].get())   #Q0.0
    snap7.util.set_bool(reading, 0, 1, switches[1].get())   #Q0.1
    snap7.util.set_bool(reading, 0, 2, switches[2].get())   #Q0.2
    snap7.util.set_bool(reading, 0, 3, switches[3].get())   #Q0.3
    snap7.util.set_bool(reading, 0, 4, switches[4].get())   #Q0.4
    plc.db_write(2, 0, reading)      
	

# Function to store data in the MySQL database
def store_data():
    data1 = int(db_spinbox.get())
    data2= int (byte_spinbox.get())
    data3=int(value_entry.get())
    data4=(data1,data2,data3)

    # Connect to the MySQL database
    db_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        database='plc1500'
    )
    db_cursor = db_connection.cursor()
    
 
    try:
        # Store data into the MySQL database
        sql= "INSERT INTO python(DataBlock,Byte,Value) VALUES (%s, %s, %s)"
        db_cursor.execute(sql, data4)
        db_connection.commit()
       
    except mysql.connector.Error as error:
        messagebox.showerror("Error", str(error))
    


    
# Create the main window
window = ttk.Window(themename='superhero')
window.title("PLC GUI")
window.geometry('720x270')

# IP Address frame
ip_frame = ttk.Frame(window)
ip_frame.pack(pady=10)

ip_label = ttk.Label(ip_frame, text="IP Address:")
ip_label.pack(side=tk.LEFT)

ip_entry = ttk.Entry(ip_frame)
ip_entry.pack(side=tk.LEFT)

connect_button = ttk.Button(ip_frame, text="Connect", command=connect_plc)
connect_button.pack(side=tk.LEFT,padx=10)


# Outputs frame
outputs_frame = ttk.LabelFrame(window, text="Outputs")
outputs_frame.pack(side=tk.LEFT,padx=15)

switches = []

for i in range(5):
    switch_label = ttk.Label(outputs_frame, text="Q0." + str(i))
    switch_label.grid(row=i, column=0)

    switch = ttk.BooleanVar()
    switch_checkbutton = ttk.Checkbutton(outputs_frame, variable=switch, style='success.TCheckbutton')
    switch_checkbutton.grid(row=i, column=1)
    switches.append(switch)

write_output_button = ttk.Button(outputs_frame, text="Write Outputs", command=writeBool)
write_output_button.grid(row=6, column=0, columnspan=2,padx=5,pady=3)

for widget in outputs_frame.winfo_children():
    widget.grid_configure(padx=3 , pady=3)


# Read Data frame
read_frame = ttk.LabelFrame(window, text="Read Data")
read_frame.pack(side=tk.LEFT,padx=15)

db_label = ttk.Label(read_frame, text="DB Number:")
db_label.grid(row=0, column=0)

dbR_spinbox = ttk.Spinbox(read_frame, from_=0, to=9999)
dbR_spinbox.grid(row=0, column=1)

byte_label = ttk.Label(read_frame, text="Byte Number:")
byte_label.grid(row=1, column=0)

byteR_spinbox = ttk.Spinbox(read_frame, from_=0, to=255)
byteR_spinbox.grid(row=1, column=1)

read_button = ttk.Button(read_frame, text="Read", command=read_data)
read_button.grid(row=2, column=0, columnspan=2)

read_label = ttk.Label(read_frame, text="", font=('Helvetica', 17))
#read_label.pack(side=tk.BOTTOM,pady=10)
read_label.grid(row=3,column=0,columnspan=2)

for widget in read_frame.winfo_children():
    widget.grid_configure(padx=5 , pady=5)


# Write Data frame
write_frame = ttk.LabelFrame(window, text="Write Data")
write_frame.pack(side=tk.LEFT,padx=15)

db_label = ttk.Label(write_frame, text="DB Number:")
db_label.grid(row=0, column=0)

db_spinbox = ttk.Spinbox(write_frame, from_=0, to=9999)
db_spinbox.grid(row=0, column=1)

byte_label = ttk.Label(write_frame, text="Byte Number:")
byte_label.grid(row=1, column=0)

byte_spinbox = ttk.Spinbox(write_frame, from_=0, to=255)
byte_spinbox.grid(row=1, column=1)

value_label = ttk.Label(write_frame, text="Value:")
value_label.grid(row=2, column=0)

value_entry = ttk.Entry(write_frame)
value_entry.grid(row=2, column=1)

# Function to execute multiple commands
def execute_multiple_commands():
    store_data()
    write_data()

write_button = ttk.Button(write_frame, text="Write", command= execute_multiple_commands )
write_button.grid(row=3, column=0, columnspan=2)


for widget in write_frame.winfo_children():
    widget.grid_configure(padx=5 , pady=5)

window.mainloop()




