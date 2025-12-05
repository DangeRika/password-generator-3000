import os
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import Tk, Toplevel, Label, Button, Entry, END, Spinbox, Radiobutton, StringVar, IntVar, LEFT, S
from tkinter import Text, Scrollbar, RIGHT, Y, BOTH
import random
import string
from datetime import datetime
import sys



"""
need tree things

1. add buttons for copy password and button for open passwords list
2. fix input length password
3. built beutiful frontend 

"""


# -- Additional windows --

# window_before_exit
window_before_exit = None

def close_main_window():
    global window_before_exit
    if window_before_exit is not None and window_before_exit.winfo_exists():
        return
    
    window_before_exit = Toplevel(main_window)
    window_before_exit.title("Confirm exit")
    window_before_exit.resizable(False,False)
    window_before_exit.grab_set()
    window_before_exit.transient(main_window)
    window_before_exit.focus_set()
    window_before_exit.protocol("WM_DELETE_WINDOW", lambda: None)
    
    def yes_exit():
        global window_before_exit
        main_window.destroy()
        window_before_exit = None
        print("closing app")
        

    def no_exit():
        global window_before_exit
        window_before_exit.destroy()
        window_before_exit = None


    #def on_hover(widget, hover_color, normal_color):
    #    widget.config(bg=hover_color)
    #    widget.bind("<Leave>", lambda x: widget.config(bg=normal_color))
    
    label = Label(window_before_exit, text="Are you sure you want to exit?")
    label.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

    # button yes    
    button_yes = Button(window_before_exit, text="Yes", bg="green", fg="black", relief="raised", borderwidth=3, width=10, command=yes_exit)
    button_yes.grid(row=1, column=0, padx=10, pady=10)

    # button no
    button_no = Button(window_before_exit, text="No", bg="red", fg="black", relief="raised", borderwidth=3, width=10, command=no_exit)
    button_no.grid(row=1, column=1, padx=10, pady=10)

    # on_hover(button_yes, "lightgreen", "green")
    # on_hover(button_no, "pink", "red")


window_before_save_password = None

def add_description_for_password(password):
    global window_before_save_password
    if window_before_save_password is not None and window_before_save_password.winfo_exists():
        return
        
    window_before_save_password = Toplevel(main_window) 
    window_before_save_password.title("Add Description")
    window_before_save_password.geometry("400x150")

    
    # Label
    description_label = Label(window_before_save_password, text="Add a description (max 15 characters):")
    description_label.pack(padx=10, pady=10)

    # Entry for description (with max length)
    description_var = StringVar()

    description_entry = Entry(window_before_save_password, textvariable=description_var, width=30)
    description_entry.pack(padx=10, pady=5)

    # Label to show the character count
    char_count_label = Label(window_before_save_password, text="Characters: 0/15")
    char_count_label.pack(padx=10)

    def counter_characters(*args):
        len_input_chars = len(description_var.get())
        char_count_label.config(text=f"Characters: {len_input_chars}/15")        
        if len_input_chars > 15:
            description_var.set(description_var.get()[:15])  # Limit to 100 chars
            char_count_label.config(text="Characters: 15/15")

    description_var.trace_add("write", counter_characters)



    def save_description_and_password():
            description = description_var.get()
            write_generated_password_to_vault(password, description)  # Save the password with description
            window_before_save_password.destroy()

    save_description_button = Button(window_before_save_password, text="Save Description", command=save_description_and_password)
    save_description_button.pack(padx=10, pady=10)



    def cancel_add_description():
        print("password was not saved")
        window_before_save_password.destroy()

    window_before_save_password.protocol("WM_DELETE_WINDOW", cancel_add_description)



window_for_passwords_list = None

def open_window_for_passwords_list():
    global window_for_passwords_list
    if window_for_passwords_list is not None and window_for_passwords_list.winfo_exists():
        return
        
    window_for_passwords_list = Toplevel(main_window) 
    window_for_passwords_list.title("My passwords")
    window_for_passwords_list.geometry("450x450")

    text_area = Text(window_for_passwords_list, wrap="none", font=("Arial", 11))
    text_area.pack(expand=True, fill=BOTH)

    scrollbar = Scrollbar(window_for_passwords_list, command=text_area.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    text_area.config(yscrollcommand=scrollbar.set)

    vault = "saved_passwords/passwords.txt"

    if os.path.exists(vault):
        with open(vault, 'r') as file:
            content = file.read()
            if content.strip() == "":
                text_area.insert("1.0", "File is empty")
            else:
                text_area.insert("1.0", content)
    else:
        text_area.insert("1.0", "File passwords.txt not found")

                
# -- Main Window --

main_window = Tk()

main_window.title("Password-Generator 3000")
main_window.geometry("500x400+450+200")
main_window.resizable(True, True)
main_window.minsize(300, 200)

# icon = PhotoImage(file = "icon2.png")
# window.iconphoto(False, icon)

main_window.configure(bg="lightgray")



# -- funcs --

password_var = StringVar()


def generate_password():
    length = length_var.get()
    difficulty = difficulty_var.get()

    if difficulty == "easy":
        chars = string.ascii_letters
    elif difficulty == "medium":
        chars = string.ascii_letters + string.digits
    else:
        chars = string.ascii_letters + string.digits + "!@_?#$%^&*" 

    password = ''.join(random.choice(chars) for _ in range(length))
    password_var.set(password)
        
    print(f"Generated password: {password}")
    
    password_entry.delete(0, END)
    password_entry.insert(0, password)



def write_generated_password_to_vault(password, description):
    os.makedirs("saved_passwords", exist_ok=True)
    vault = "saved_passwords/passwords.txt"

    date_and_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    description = description if description else "No description" 
    
    with open(vault, "a") as passwd_file:
        passwd_file.write(f"{date_and_time} | {password} | {description}\n") # тут запись в файл

    print("Password was saved success")



def save_generated_password():
    password = password_var.get()
    if password:
        print("Password ready to be saved, waiting for description...")
        add_description_for_password(password)
    else:
        print("No password generated yet")

    

def copy_generated_password():
    pass



def open_passwords_list():
    open_window_for_passwords_list()



# -- Widgets --


# add frame for all widgets!!


label = Label(text="Сгенерируй пароль!")
label.pack()



length_label = Label(main_window, text="Введите длину пароля:").pack()


# choice lentgh password
length_var = IntVar(value=12)
Spinbox(main_window, from_=4, to=20, textvariable=length_var, validate='key').pack()


# choice difficult password 
difficulty_var = StringVar(value="easy")  # easy, medium, hard

Radiobutton(main_window, text="Easy", variable=difficulty_var, value="easy").pack()
Radiobutton(main_window, text="Medium", variable=difficulty_var, value="medium").pack()
Radiobutton(main_window, text="Hard", variable=difficulty_var, value="hard").pack()


# generate password
button_generetion_password = ttk.Button()
button_generetion_password.pack(padx=20)
button_generetion_password.config(text="Сгенерировать пароль", command=generate_password)


password_entry = Entry(main_window, font=("Arial", 14), width=25)
password_entry.pack(pady=10)



# image for save button
img = Image.open("icons/save_button.png")
img = img.resize((28, 28), Image.LANCZOS)   # ставь любой размер

save_icon = ImageTk.PhotoImage(img)
# save password
save_generetion_password = ttk.Button()
save_generetion_password.config(image=save_icon, command=save_generated_password)
save_generetion_password.image = save_icon
save_generetion_password.pack(padx=20)


# image for copy button
img = Image.open("icons/copy_button.png")
img = img.resize((28, 28), Image.LANCZOS)

copy_icon = ImageTk.PhotoImage(img)
# copy password
button_copy_password = ttk.Button()
button_copy_password.config(image=copy_icon, command=copy_generated_password)
button_copy_password.image = copy_icon
button_copy_password.pack(padx=20)


# image for copy button
img = Image.open("icons/passwords_list_button.png")
img = img.resize((28, 28), Image.LANCZOS)

passwords_list_icon = ImageTk.PhotoImage(img)
# open passwords list
button_open_passwords_list = ttk.Button()
button_open_passwords_list.config(image=passwords_list_icon, command=open_passwords_list)
button_open_passwords_list.image = passwords_list_icon
button_open_passwords_list.pack(padx=20)


# ---------------------


main_window.update_idletasks()

main_window.protocol("WM_DELETE_WINDOW", close_main_window)



def on_escape(event):
    close_main_window()

# Привязываем клавишу Escape (Esc) к функции on_escape
main_window.bind('<Escape>', on_escape)


main_window.mainloop()



