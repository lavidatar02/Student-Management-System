from tkinter import *
import time
import ttkthemes
from tkinter import ttk, messagebox, filedialog
import pymysql
import pandas


# ================= FUNCTIONALITY PART =================

def exit():
    result = messagebox.askyesno('Confirm', 'Do you want to exit?')
    if result:
        root.destroy()


def export_data():
    url = filedialog.asksaveasfilename(defaultextension='.csv')

    if not url:
        return

    indexing = studentTable.get_children()
    newlist = []

    for index in indexing:
        content = studentTable.item(index)
        datalist = content['values']
        newlist.append(datalist)

    table = pandas.DataFrame(
        newlist,
        columns=['Id', 'Name', 'Mobile', 'Email', 'Address', 'Gender', 'DOB', 'Added Date', 'Added Time'])

    table.to_csv(url, index=False)

    messagebox.showinfo('Success','Data is saved successfully')


def toplevel_data(title, button_text, command):
    global idEntry, phoneEntry, nameEntry
    global emailEntry, addressEntry, genderEntry
    global dobEntry, screen

    screen = Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(False, False)

    idLabel = Label(
        screen,
        text='Id',
        font=('times new roman', 20, 'bold')
    )
    idLabel.grid(row=0, column=0, padx=20, pady=15, sticky=W)

    idEntry = Entry(
        screen,
        font=('times new roman', 15, 'bold'), width=24 )

    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(
        screen,
        text='Name',
        font=('times new roman', 20, 'bold')
    )

    nameLabel.grid( row=1, column=0, padx=20, pady=15, sticky=W)

    nameEntry = Entry(
        screen,
        font=('times new roman', 15, 'bold'), width=24
    )
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    phoneLabel = Label(
        screen,
        text='Phone',
        font=('times new roman', 20, 'bold')
    )
    phoneLabel.grid( row=2, column=0, padx=20, pady=15, sticky=W)

    phoneEntry = Entry(
        screen,
        font=('times new roman', 15, 'bold'), width=24
    )

    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    emailLabel = Label(
        screen,
        text='Email',
        font=('times new roman', 20, 'bold')
    )

    emailLabel.grid(row=3, column=0, padx=20, pady=15, sticky=W)

    emailEntry = Entry(
        screen,
        font=('times new roman', 15, 'bold'), width=24
    )

    emailEntry.grid(row=3, column=1, pady=15, padx=10 )

    addressLabel = Label(
        screen,
        text='Address',
        font=('times new roman', 20, 'bold')
    )

    addressLabel.grid(row=4, column=0, padx=20, pady=15, sticky=W)

    addressEntry = Entry(
        screen,
        font=('times new roman', 15, 'bold'), width=24
    )

    addressEntry.grid(row=4, column=1, pady=15, padx=10)

    genderLabel = Label(
        screen,
        text='Gender',
        font=('times new roman', 20, 'bold')
    )

    genderLabel.grid(row=5, column=0, padx=20, pady=15, sticky=W)

    genderEntry = Entry(
        screen,
        font=('times new roman', 15, 'bold'), width=24
    )

    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    dobLabel = Label(
        screen,
        text='D.O.B',
        font=('times new roman', 20, 'bold')
    )

    dobLabel.grid(row=6, column=0, padx=20, pady=15, sticky=W)

    dobEntry = Entry(
        screen,
        font=('times new roman', 15, 'bold'), width=24
    )
    dobEntry.grid(row=6, column=1, pady=15, padx=10)

    student_button = ttk.Button(
        screen,
        text=button_text,
        command=command
    )

    student_button.grid(row=7, columnspan=2, pady=15)

    if title == 'Update Student':
        indexing = studentTable.focus()

        if not indexing:
            messagebox.showwarning(
                'Warning',
                'Please select a student first',
                parent=screen
            )
            screen.destroy()
            return

        content = studentTable.item(indexing)
        listdata = content['values']

        idEntry.insert(0, listdata[0])
        nameEntry.insert(0, listdata[1])
        phoneEntry.insert(0, listdata[2])
        emailEntry.insert(0, listdata[3])
        addressEntry.insert(0, listdata[4])
        genderEntry.insert(0, listdata[5])
        dobEntry.insert(0, listdata[6])


def update_data():
    query = '''
        update student
        set name=%s, mobile=%s, email=%s, address=%s, gender=%s, dob=%s, date=%s, time=%s
        where id=%s
    '''

    mycursor.execute(
        query,
        (nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(), dobEntry.get(), date,
         currenttime,
            idEntry.get()
        )
    )

    con.commit()

    messagebox.showinfo(
        'Success',
        f'Id {idEntry.get()} is modified successfully',
        parent=screen
    )

    screen.destroy()
    show_student()


def show_student():
    query = 'select * from student'

    mycursor.execute(query)

    fetched_data = mycursor.fetchall()

    studentTable.delete(
        *studentTable.get_children()
    )

    for data in fetched_data:
        studentTable.insert(
            '',
            END,
            values=data
        )


def delete_student():
    indexing = studentTable.focus()

    if not indexing:
        messagebox.showwarning(
            'Warning',
            'Please select a student first'
        )
        return

    content = studentTable.item(indexing)
    content_id = content['values'][0]

    query = 'delete from student where id=%s'

    mycursor.execute(
        query,
        (content_id,)
    )

    con.commit()

    messagebox.showinfo(
        'Deleted',
        f'This {content_id} is deleted successfully'
    )

    show_student()


def search_data():
    query = '''
        select * from student
        where id=%s or name=%s or mobile=%s or email=%s or address=%s or gender=%s or dob=%s'''

    mycursor.execute(
        query,
        (idEntry.get(), nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(),
             dobEntry.get())
    )

    studentTable.delete(
        *studentTable.get_children()
    )

    fetched_data = mycursor.fetchall()

    for data in fetched_data:
        studentTable.insert(
            '',
            END,
            values=data
        )


def add_data():
    if (
        idEntry.get() == '' or
        nameEntry.get() == '' or
        phoneEntry.get() == '' or
        emailEntry.get() == '' or
        addressEntry.get() == '' or
        genderEntry.get() == '' or
        dobEntry.get() == ''
    ):
        messagebox.showerror(
            'Error',
            'All Fields are required',
            parent=screen
        )

    else:
        try:
            query = '''
                insert into student
                values(%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''

            mycursor.execute(
                query,
                (idEntry.get(), nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(),
                      dobEntry.get(), date, currenttime)
            )

            con.commit()

            result = messagebox.askyesno(
                'Confirm',
                'Data added successfully. Do you want to clean the form?',
                parent=screen
            )

            if result:
                idEntry.delete(0, END)
                nameEntry.delete(0, END)
                phoneEntry.delete(0, END)
                emailEntry.delete(0, END)
                addressEntry.delete(0, END)
                genderEntry.delete(0, END)
                dobEntry.delete(0, END)

        except:
            messagebox.showerror(
                'Error',
                'Id cannot be repeated',
                parent=screen
            )
            return

        show_student()


def connect_database():

    def connect():
        global mycursor, con

        try:
            con = pymysql.connect(
                host=hostEntry.get(),
                user=usernameEntry.get(),
                password=passwordEntry.get()
            )

            mycursor = con.cursor()

        except:
            messagebox.showerror(
                'Error',
                'Invalid Details',
                parent=connectWindow
            )
            return

        try:
            query = 'create database studentmanagementsystem'
            mycursor.execute(query)

            query = 'use studentmanagementsystem'
            mycursor.execute(query)

            query = '''create table student(id int not null primary key, name varchar(30), mobile varchar(15), email varchar(100), 
                address varchar(100), gender varchar(20), dob varchar(20), date varchar(50), time varchar(50))'''

            mycursor.execute(query)

        except:
            query = 'use studentmanagementsystem'
            mycursor.execute(query)

        messagebox.showinfo(
            'Success',
            'Database Connection is successful',
            parent=connectWindow
        )

        connectWindow.destroy()

        addstudentButton.config(state=NORMAL)
        searchstudentButton.config(state=NORMAL)
        updatestudentButton.config(state=NORMAL)
        showstudentButton.config(state=NORMAL)
        exportdataButton.config(state=NORMAL)
        deletestudentButton.config(state=NORMAL)

    connectWindow = Toplevel()

    connectWindow.grab_set()

    connectWindow.geometry('470x250+730+230')

    connectWindow.title('Database Connection')

    connectWindow.resizable(0,0)

    hostnameLabel = Label(
        connectWindow,
        text='Host Name',
        font=('arial', 20, 'bold')
    )

    hostnameLabel.grid(row=0, column=0, padx=20)

    hostEntry = Entry(
        connectWindow,
        font=('roman', 15, 'bold'), bd=2
    )

    hostEntry.grid(row=0, column=1, padx=40, pady=20)

    usernameLabel = Label(
        connectWindow,
        text='User Name',
        font=('arial', 20, 'bold')
    )

    usernameLabel.grid(row=1, column=0, padx=20)

    usernameEntry = Entry(
        connectWindow,
        font=('roman', 15, 'bold'), bd=2
    )

    usernameEntry.grid(row=1, column=1, padx=40, pady=20)

    passwordLabel = Label(
        connectWindow,
        text='Password',
        font=('arial', 20, 'bold')
    )

    passwordLabel.grid(row=2, column=0, padx=20)

    passwordEntry = Entry(
        connectWindow,
        font=('roman', 15, 'bold'), bd=2
    )

    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    connectButton = ttk.Button(
        connectWindow,
        text='CONNECT',
        command=connect
    )

    connectButton.grid(row=3, columnspan=2)


# ================= SLIDER =================

count = 0
text = ''


def slider():
    global text, count

    if count == len(s):
        count = 0
        text = ''

    text = text + s[count]

    sliderLable.config(
        text=text
    )

    count += 1

    sliderLable.after(
        300,
        slider
    )


# ================= CLOCK =================

def clock():
    global date, currenttime

    date = time.strftime(
        '%d/%m/%Y'
    )

    currenttime = time.strftime(
        '%I:%M:%S%p'
    )

    datetimeLabel.config(
        text=f'Date:{date}\nTime:{currenttime}'
    )

    datetimeLabel.after(
        1000,
        clock
    )


# =========================================================
#                         GUI PART
# =========================================================

root = ttkthemes.ThemedTk()

root.get_themes()

root.set_theme('radiance')

root.geometry('1174x700+0+0')

root.state('zoomed')

root.resizable(True,True)

root.title('Student Management System')


# ================= WINDOW GRID =================

root.grid_rowconfigure(1,weight=1)

root.grid_columnconfigure(1,weight=1)


# ================= DATE & TIME =================

datetimeLabel = Label(
    root,
    text='hello',
    font=('Times New Roman', 18, 'bold')
)

datetimeLabel.place(x=5, y=5)

clock()


# ================= TITLE =================

s = 'Student Management System'

sliderLable = Label( root, font=('Arial', 28, 'italic bold'))

sliderLable.place(relx=0.5, y=0,anchor='n')

slider()


# ================= CONNECT DATABASE =================

connectButton = ttk.Button(
    root,
    text='Connect database',
    command=connect_database
)

connectButton.place( relx=0.98, y=10, anchor='ne')


# ================= LEFT FRAME =================

leftFrame = Frame(root)

leftFrame.grid(row=1, column=0, padx=25, pady=(70, 20), sticky='ns')

leftFrame.grid_columnconfigure(0, weight=1)


# ================= LOGO =================

logo_image = PhotoImage(file='student.png')

logo_Label = Label(leftFrame, image=logo_image)

logo_Label.grid(row=0, column=0, pady=(0, 20))


# =========================================================
#                 BUTTON SPACING
# =========================================================

BUTTON_GAP = 18


# ================= BUTTONS =================

addstudentButton = ttk.Button(
    leftFrame,
    text='Add Student', width=25, state=DISABLED,
    command=lambda: toplevel_data(
        'Add Student', 'Add',
        add_data
    )
)

addstudentButton.grid(row=1, column=0, pady=BUTTON_GAP, sticky='ew')


searchstudentButton = ttk.Button(
    leftFrame,
    text='Search Student',
    width=25,
    state=DISABLED,
    command=lambda: toplevel_data(
        'Search Student',
        'Search',
        search_data
    )
)

searchstudentButton.grid(row=2, column=0, pady=BUTTON_GAP, sticky='ew')


deletestudentButton = ttk.Button(
    leftFrame,
    text='Delete Student',
    width=25,
    state=DISABLED,
    command=delete_student
)

deletestudentButton.grid(row=3, column=0, pady=BUTTON_GAP, sticky='ew')


updatestudentButton = ttk.Button(
    leftFrame,
    text='Update Student',
    width=25,
    state=DISABLED,
    command=lambda: toplevel_data(
        'Update Student',
        'Update',
        update_data
    )
)

updatestudentButton.grid(row=4, column=0, pady=BUTTON_GAP, sticky='ew')


showstudentButton = ttk.Button(
    leftFrame,
    text='Show Student',
    width=25,
    state=DISABLED,
    command=show_student
)

showstudentButton.grid(row=5, column=0, pady=BUTTON_GAP, sticky='ew')


exportdataButton = ttk.Button(
    leftFrame,
    text='Export Data',
    width=25,
    state=DISABLED,
    command=export_data
)

exportdataButton.grid(row=6, column=0, pady=BUTTON_GAP, sticky='ew')


exitButton = ttk.Button(
    leftFrame,
    text='Exit',
    width=25,
    command=exit
)

exitButton.grid(row=7, column=0, pady=BUTTON_GAP, sticky='ew')


# ================= RIGHT FRAME =================

rightFrame = Frame(root)

rightFrame.grid(row=1, column=1, padx=(20, 30), pady=(70, 20), sticky='nsew')

rightFrame.grid_rowconfigure(0,weight=1)

rightFrame.grid_columnconfigure(0,weight=1)

# ================= SCROLLBARS =================

scrollBarX = Scrollbar(rightFrame,orient=HORIZONTAL)

scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

# ================= STUDENT TABLE =================

studentTable = ttk.Treeview(
    rightFrame,
    columns=('Id', 'Name', 'Mobile', 'Email', 'Address', 'Gender', 'D.O.B', 'Added Date', 'Added Time'),
    xscrollcommand=scrollBarX.set,
    yscrollcommand=scrollBarY.set
)


scrollBarX.config(command=studentTable.xview)

scrollBarY.config(command=studentTable.yview)


scrollBarX.grid(row=1, column=0, sticky='ew')

scrollBarY.grid(row=0, column=1, sticky='ns')

studentTable.grid(row=0, column=0, sticky='nsew')


# ================= TABLE HEADINGS =================

studentTable.heading('Id', text='Id')

studentTable.heading('Name', text='Name')

studentTable.heading('Mobile', text='Mobile No.')

studentTable.heading('Email', text='Email Address')

studentTable.heading('Address', text='Address')

studentTable.heading('Gender', text='Gender')

studentTable.heading('D.O.B', text='D.O.B')

studentTable.heading('Added Date', text='Added Date')

studentTable.heading('Added Time', text='Added Time')


# ================= TABLE COLUMNS =================

studentTable.column('Id', width=70, anchor=CENTER)

studentTable.column('Name', width=250, anchor=CENTER)

studentTable.column('Mobile', width=180, anchor=CENTER)

studentTable.column('Email', width=280, anchor=CENTER)

studentTable.column('Address', width=280, anchor=CENTER)

studentTable.column('Gender', width=150, anchor=CENTER)

studentTable.column('D.O.B', width=150, anchor=CENTER)

studentTable.column('Added Date', width=150, anchor=CENTER)

studentTable.column('Added Time', width=150, anchor=CENTER)


# ================= TABLE STYLE =================

style = ttk.Style()

style.configure('Treeview', rowheight=40, font=('Arial', 12, 'bold'), background='#F8F8F8', fieldbackground='white')

style.configure('Treeview.Heading', font=('Arial', 14, 'bold'))

studentTable.config(show='headings')


# ================= START =================

root.mainloop()
