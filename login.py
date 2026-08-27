from tkinter import *
from tkinter import messagebox
from PIL import ImageTk


def login():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'Fields cannot be empty')

    elif usernameEntry.get() == 'lavi' and passwordEntry.get() == 'lavi':
        messagebox.showinfo('Success', 'Welcome')
        window.destroy()
        import sms

    else:
        messagebox.showerror('Error', 'Please enter correct details')


window = Tk()

window.title('Login System of Student Management System')

#Open Window in full Screen/maximized mode
window.state('zoomed')
#set the normal/restored window size
window.geometry('1280x700+0+0')
window.resizable(True, True)

# Background Image
backgroundImage = ImageTk.PhotoImage(file='bg.png')

bgLabel = Label(window, image=backgroundImage)
bgLabel.place(x=0, y=0)


# Login Frame
loginFrame = Frame(window, bg='#FAFAFA')
loginFrame.place(x=500, y=300)


# Logo
logoImage = PhotoImage(file='logo.png')

logoLabel = Label(
    loginFrame,
    image=logoImage,
    bg='#FAFAFA',          # Same background as frame
    borderwidth=0
)
logoLabel.grid(row=0, column=0, columnspan=2, pady=10)


# Username
usernameImage = PhotoImage(file='user.png')

usernameLabel = Label(
    loginFrame,
    image=usernameImage,
    text='Username',
    compound=LEFT,
    font=('times new roman', 20, 'bold'),
    bg='#FAFAFA'
)
usernameLabel.grid(row=1, column=0, pady=10, padx=20)


usernameEntry = Entry(
    loginFrame,
    font=('times new roman', 20, 'bold'),
    bd=5,
    fg='black'
)
usernameEntry.grid(row=1, column=1, pady=10, padx=20)


# Password
passwordImage = PhotoImage(file='password.png')

passwordLabel = Label(
    loginFrame,
    image=passwordImage,
    text='Password',
    compound=LEFT,
    font=('times new roman', 20, 'bold'),
    bg='#FAFAFA'
)
passwordLabel.grid(row=2, column=0, pady=10, padx=20)


passwordEntry = Entry(
    loginFrame,
    font=('times new roman', 20, 'bold'),
    bd=5,
    fg='black'
)
passwordEntry.grid(row=2, column=1, pady=10, padx=20)


# Login Button
loginButton = Button(
    loginFrame,
    text='Login',
    font=('times new roman', 14, 'bold'),
    width=15,
    fg='white',
    bg='cornflower blue',
    activebackground='cornflower blue',
    activeforeground='white',
    cursor='hand2',
    command=login
)
loginButton.grid(row=3, column=1, pady=10)


window.mainloop()
