################################################################
from tkinter import *
from tkinter.scrolledtext import *
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import playsound

################################################################

chat_key ={
  # You have to add here chat_key json file from firebase project.
}

cred = credentials.Certificate(chat_key)
firebase_admin.initialize_app(cred,{
    'databaseURL': "" # space for firebase project url.
})

# This connects firebase real timedatabase to take or add information in it

ref = db.reference("/")


last_id = 0
last_db = {}
lst = []
last_lst = []

# Creating Tkinter window
root = Tk()
root.title("Zelda-Chat")
root.geometry("200x100")

# Creating menu
my_menu = Menu(root)
root.config(menu=my_menu)


def Chat(username,text):
    """
    This one adds message to the database, which
    contains username and the text-message.

    For example if our username is test and text is just text.
    if we run this function, it will add "test: text" to the database.
    """
    chat_ref = ref.child("Chat")
    chat_ref.push({username: text})

def server(text):
    """
    This one is for server message. if someone connects or leaves chat
    server will say about that.
    """
    ch_ref = ref.child("Chat")
    ch_ref.push({"Server": str(user)+text})

def clear():
    """
    This one will remove all the message from database and write
    "Server reloaded. All the messages are deleted!" instead of.
    """
    ch_ref = ref.child("Chat")
    ch_ref.set({})
    ch_ref.push({"Server": "Server reloaded. All the messages are deleted!"})

def chat_window():
    """
    This creates new window, when the authorization ends successfully.
    """

    global lst, last_db, last_lst
    def get_txt():
        """
        It takes the whole text from the database and writes in the list.

        To comes out on the window in next
        """
        global lst, last_db
        db = ref.get()
        if last_db != db:
            last_db = db
            for i in db['Chat'].keys():
                name = list(db['Chat'][i].keys())[0]
                lst.append(name + ":" + db['Chat'][i][name])
            return lst[-1]

    def change_text():
        """
        It adds new information in the textbox of the window. in the result,
        text shows up on the window.

        We can scroll it, or edit it.

        Also this is artificial loop, which means that messages will be livestreamed at the textbox, before
        you close the window.
        """
        my_text = get_txt()

        if my_text is not None:
            try:
                TextBox.insert(END, my_text+"\n"+"\n")
                TextBox.yview(END)

            except:pass
            else:
                """
                if you are writting the message and it shows up on the window,
                the voice does not comes up. but if you minimalize window and someone texts something
                the it plays sound.mp3, which tells you that new message shows up and you will miss that.
                """
                if user != my_text[:len(user)] or my_text[len(user)] != ":":
                    if cht.wm_state() == 'iconic':
                        # you have to add sound.mp3 file in the folder to work this line of the code
                        playsound.playsound("sound.mp3")

        root.after(1000, change_text)

    def go(event):
        """
        After pressing enter this functions runs.

        which takes text written in the textEntry and clear whole enrty.
        After that it will call chat funciton and that one will sends you message
        to the database.

        if you write "/cls" it will remove entire text messages in the database.
        """
        msg = textEntry.get()
        if msg != "":
            textEntry.delete(0, 'end')
            if msg == "/cls":
                clear()
            else:
                Chat(user,msg)

    # this one tell to the server that you connected.
    server(" Has connected!")

    # Creating of the new window
    cht = Toplevel()
    cht.title("Zelda-Chat")
    cht.geometry("500x400")
    cht.configure(bg='gray')
    TextBox = ScrolledText(cht, height='30', width='55', wrap=WORD)

    # Making entry to write message in it.
    textEntry = Entry(cht, width=150, borderwidth=1)

    # if you press the enter button go functuon will be called.
    cht.bind("<Return>", go)
    textEntry.pack(side=BOTTOM)


    # It takes the whole chat form the database and adds on the textbox
    db = ref.get()
    for i in db['Chat'].keys():
        name = list(db['Chat'][i].keys())[0]
        last_lst.append(name + ":" + db['Chat'][i][name])

    for j in range(len(last_lst)):
        if last_lst[j] != last_lst[-1]:
            TextBox.insert(END, str(last_lst[j])+"\n"+"\n")
            TextBox.yview(END)

    # call the endless loop
    change_text()
    TextBox.pack()


def create_users_passwords():
    """
    This one takes all the users and passwords from the database and writes in the list.

    it returns that list to check user and his password.
    """
    users_passwords = {}
    db = ref.get()
    for ID in db['Users'].keys():
        name = str(list(db['Users'][ID].keys())[0])
        passw = str(db['Users'][ID][name])
        users_passwords[name] = passw
    return users_passwords

def singIn():
    """
    This one takes username and password. then checks if this kind of password exists
    in the database.

    If user exists it will opens chat window. but if user does not exist, then is comes up
    error message.
    """
    global user
    user = username.get()
    passw = password.get()
    up = create_users_passwords()
    if not user in list(up.keys()):
        Label(root,text="    User doesn't exist.    ", fg="red").grid(row=3, column=0,  columnspan=3)
    else:
        if passw == up[user]:
            Label(root, text="Signed in successfully", fg="green").grid(row=3, column=0, columnspan=3)
            root.wm_state('iconic')
            chat_window()
        else:
            # if user exists but password is incorrect. it will writes that.
            Label(root, text="Password is incorrect.", fg="red").grid(row=3, column=0, columnspan=3)

def get_last_id():
    """
    This one is to get the last id in the database users list.

    We need the last id, becouse the new user id will be the last id + 1.
    """
    db = ref.get()
    for i in list(db['Users'].keys()):
        l_id = i
    return int(l_id) + 1

def registration():
    """
    It starts new window for sign up.
    """
    # enters is for empty spaces at the error massage.
    enters = "                                                                                                 "
    signup = Tk()
    signup.title("Sign Up")
    signup.geometry("420x100")

    def error(error):
        """
        It writes error messages at the regisration window.

        for example if password contains spaces, it will writes that.
        """
        error_message['fg'] = "red"
        error_message['text'] = enters
        def make_error():
            error_message['text'] = error
        signup.after(30, make_error)



    def singUp():
        user = reg_user.get()
        passw = reg_pass.get()
        if user != "" and passw != "":
            if not " " in user and not " " in passw:
                if len(user) > 3 and len(passw) > 6:
                    up = create_users_passwords()
                    if not user in list(up.keys()):
                        last_id = get_last_id()
                        hopper_ref = ref.child('Users')
                        hopper_ref.update({str(last_id): {user: passw}})
                        error_message['fg'] = "green"
                        error_message['text'] = "You signed up successfully."
                    else:
                        error("This username already exists.")
                else:
                    error("The length of the username should be more than 3 and password should be more than 6")
            else:
                error("You can not use spaces in the username or password")
        else:
            error("Please fill all the fields")

    """
    Code down below is for entrys and text to the user to understand that entry is for.
    """
    Label(signup, text="Username: ").grid(row=0, column=0)
    Label(signup, text="Password: ").grid(row=1, column=0)

    reg_user = Entry(signup, width=20, borderwidth=1)
    reg_pass = Entry(signup, width=20, borderwidth=1)

    reg_user.grid(row=0,column=1)
    reg_pass.grid(row=1,column=1)

    Button(signup, text="SignUp", bg="green", padx=20, pady=1, borderwidth=1, command=singUp).grid(row=2, column=1)
    error_message = Label(signup, text="", fg="red")
    error_message.grid(row=3, column=0, columnspan=400)


"""
Code down below is for entrys and text to the user to understand that entry is for.

it places the button, entrys on the window.
"""

Label(root, text="Username: ").grid(row=0,column=0)
Label(root, text="Password: ").grid(row=1,column=0)

username = Entry(root, width=20, borderwidth=1)
password = Entry(root, width=20, borderwidth=1)

username.grid(row=0,column=1)
password.grid(row=1,column=1)

Button(root, text="SignIn", bg="green", padx=20, pady=1, borderwidth=1, command=singIn).grid(row=2,column=1)

file_menu = Menu(my_menu)
admin_menu = Menu(my_menu)

my_menu.add_cascade(label="Menu", menu=file_menu)
file_menu.add_command(label="SignUp", command=registration)
file_menu.add_command(label="Exit", command=root.quit)

root.mainloop()

# when you close all the windows. server will writes that you left the chat.
server(" Has left!")