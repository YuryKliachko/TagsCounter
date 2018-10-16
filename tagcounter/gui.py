from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tagcounter.counter import *
import yaml
import threading
import time
from multiprocessing import Process, Queue

if __name__=='__main__':
    root = Tk()

    #This func retrieves aliases from "aliases.yaml" and returns them as a Python dictionary
    #If the file is not found, it returns None

    def get_alias_dict():
        alias_dict = {}
        try:
            with open("aliases.yaml") as aliases:
                data = yaml.load(aliases)
                for alias, name in data.items():
                    alias_dict[alias] = name
            return alias_dict
        except FileNotFoundError:
            return None

    #This func takes an alias delected in the combobox and put it into the name field, which is cleaned in advance

    def put_alias_in_field(event):
        alias = combobox.get()
        name_field.delete(0, END)
        name_field.insert(INSERT, alias)
        result_field.delete(1.0, END)
        tvar.set('')

    #This func firstly checks if user has entered a name if a source to be find. If yes, checks whether the name is alias
    #or not. In case it's an alias, takes a domain name associated with the alias and launches getting tags process.
    #If the name is not an alias, it accepts the name as a domain name and launches getting tags method.
    #Tags obtained are uploaded to the database at once.

    def get_tags():
        result_field.delete(1.0, END)
        tvar.set("")
        user_entry = name_field.get()
        if user_entry != "":
            name_by_alias = alias_dict.get(user_entry)
            if name_by_alias is None:
                    name = user_entry
            else:
                name = name_by_alias
            result = count_tags(domain_name=name)
            if result is not None:
                upload_to_db(domain_name=name, url=result["url"],date=result["date"], tagdict=result["tagdict"])
                for key, value in sorted(result["tagdict"].items()):
                    data = q.put("{}: {} opening tags and {} closing tags\n".format(key, value[0], value[1]))
                    #result_field.insert(INSERT, "{}: {} opening tags and {} closing tags\n".format(key, value[0], value[1]))
                    time.sleep(0.5)
                tvar.set("Tags successfully obtained!")
            else:
                tvar.set("Tags has not beeen obtained!")
        else:
            result_field.insert(INSERT, "Select the name of the source to be found\n")
            time.sleep(0.5)

    #This func is similar to get_tags() one, but tags are retrieved from the database

    def retrieve_tags(event):
        result_field.delete(1.0, END)
        tvar.set("")
        user_entry = name_field.get()
        if user_entry != '':
            name_by_alias = alias_dict.get(user_entry)
            if name_by_alias is None:
                    name = user_entry
            else:
                name = name_by_alias
            result = retrieve_by_name(domain_name=name)
            if result is not None:
                for key, value in sorted(result["tagdict"].items()):
                    result_field.insert(INSERT, "{}: {} opening tags and {} closing tags\n".format(key, value[0], value[1]))
                    time.sleep(2)
                tvar.set("Tags successfully obtained!")
            else:
                result_field.insert(INSERT, "The source has not been found in database\n")
        else:
            result_field.insert(INSERT, "Select the name of the source to be found\n")
            time.sleep(2)

    #Elements of the app window

    root.title("Tags Counter")

    alias_dict = get_alias_dict()

    label_1 = Label(root, text="Choose the name of the source:", font="Callibri")
    label_1.grid(row=0, column=0, sticky=E)

    combobox = ttk.Combobox(root)
    if alias_dict is not None:
        combobox["values"] = [alias for alias in alias_dict.keys()]
    else:
        messagebox.showerror('File not found', 'File with aliases has not been found. Create a new aliases.yaml file to use predefined names.')
        combobox.config(state="disabled")
    combobox.current()
    combobox.grid(row=0, column=1, sticky=W)
    combobox.bind("<<ComboboxSelected>>", put_alias_in_field)

    label_2 = Label(root, text="or enter the name manually:")
    label_2.grid(row=1, column=0, sticky=E)

    name_field = Entry(root)
    name_field.grid(row=1, column=1, sticky=W)

    thread = Process(target=get_tags)
    q = Queue()
    def new_thread(event):
        thread.daemon = True
        thread.start()

    def stop(event):
        thread.terminate()
        print('ghgh')

    def check_queue():
        while True:
            try:
                data = q.get()
                result_field.insert(INSERT, data)
                root.update()
            except:
                break

    load_button = Button(root, text="LOAD")
    load_button.grid(row=3, sticky=W)
    load_button.bind('<Button-1>', new_thread)

    retrieve_button = Button(root, text="GET FROM DATABASE")
    retrieve_button.grid(row=3, column=1, sticky=W)
    retrieve_button.bind("<Button-1>", retrieve_tags)

    stop_button = Button(root, text="STOP")
    stop_button.grid(row=3, column=2, sticky=W)
    stop_button.bind('<Button-1>', stop)

    result_field = Text(root, width=60, height=30, wrap=WORD, borderwidth=2, relief="groove")
    result_field.grid(row=4, columnspan=2, sticky=W)

    tvar = StringVar()
    status_label = Label(root, textvariable=tvar)
    status_label.grid(row=5, column=0, sticky=W)

    root.mainloop()