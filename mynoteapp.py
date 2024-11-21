import tkinter as tk
from tkinter import ttk, messagebox
import json
from ttkbootstrap import Style


#creating main window
root = tk.Tk()
root.title("Aritra's Note App")
root.geometry("515x515")

#Configuring style
style = Style(theme="darkly")
style = ttk.Style()

#Configure font for tabs
style.configure("TNotebook.Tab", font=("TkDefaultFont", 14, "bold"))

#setting background color : dark
root.configure(bg="#333333")

#create notebook 
notebook = ttk.Notebook(root, style="TNotebook")

#Load previously saved notes. Since no data base is used, we have to save the notes in a json
notes = {}
try:
    with open("app_notes.json", "r") as f:
        notes = json.load(f)
except FileNotFoundError:
    pass

#Create and pack notebook widget
notebook = ttk.Notebook(root)
notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

#method to add new note
def add_note():
    #Create frame for a new note
    note_frame = ttk.Frame(notebook, padding=10)
    notebook.add(note_frame, text="New Note")

    #Widgets for note title and content
    title_label = ttk.Label(note_frame, text="Title: ", foreground="white", background="#333333")
    title_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")

    title_entry = ttk.Entry(note_frame, width=40, foreground="white", background="#444444")
    title_entry.grid(row=0, column=1, padx=10, pady=10)

    content_label = ttk.Label(note_frame, text="Content: ", foreground="white", background="#333333")
    content_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")

    content_entry = tk.Text(note_frame, width=40, height=10, foreground="white", background="#444444")
    content_entry.grid(row=1, column=1, padx=10, pady=10)

    #method to save note
    def save_note():
        #get title and content
        title = title_entry.get()
        content = content_entry.get("1.0", tk.END)

        #Add notes to dictionary
        notes[title] = content.strip()

        #Save notes to json file
        with open("app_notes.json", "w") as f:
            json.dump(notes, f)
        
        #add note to notebook
        note_content = tk.Text(notebook, width=40, height=10, foreground="white", background="#444444")
        note_content.insert(tk.END, content)
        notebook.forget(notebook.select())
        notebook.add(note_content, text=title)

    
    save_button = ttk.Button(note_frame, text="Save Note",
                                command=save_note, style="secondary.TButton")
    save_button.grid(row=2, column=0, padx=10, pady=10)



#method to Load notes
def load_notes():
    try:
        with open("app_notes.json", "r") as f:
            notes = json.load(f)
        
        for title, content in notes.items():
            note_content = tk.Text(notebook, width=40, height=10)
            note_content.insert(tk.END, content)
            notebook.add(note_content, text=title)
    
    except FileNotFoundError:
        pass

#load notes at start
load_notes()

#edit notes

def edit_note():
    #get the current tab index
    current_tab = notebook.index(notebook.select())

    #get note title
    note_title = notebook.tab(current_tab, "text")
    #get note content
    note_content = notes[note_title]

    #Create frame for editing note
    note_frame = ttk.Frame(notebook, padding=10)
    notebook.forget(current_tab)
    notebook.add(note_frame, text=f"Edit Note: {note_title}")

    #Widgets for note title and content
    title_label = ttk.Label(note_frame, text="Title: ", foreground="white", background="#333333")
    title_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")

    title_entry = ttk.Entry(note_frame, width=40, foreground="white", background="#444444")
    title_entry.insert(tk.END, note_title)
    title_entry.grid(row=0, column=1, padx=10, pady=10)

    

    content_label = ttk.Label(note_frame, text="Content: ", foreground="white", background="#333333")
    content_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")

    content_entry = tk.Text(note_frame, width=40, height=10, foreground="white", background="#444444")
    content_entry.insert(tk.END, note_content)
    content_entry.grid(row=1, column=1, padx=10, pady=10)

    #method to save note
    def save_edited_note():

        #while saving the edited version of the note, we have pop the existing note dictionary from the json file using the older title key
        notes.pop(note_title)
        #get title and content
        title = title_entry.get()
        content = content_entry.get("1.0", tk.END)

        #Add notes to dictionary
        notes[title] = content.strip()

        #Save notes to json file
        with open("app_notes.json", "w") as f:
            json.dump(notes, f)
        
        #add note to notebook
        note_content = tk.Text(notebook, width=40, height=10, foreground="white", background="#444444")
        note_content.insert(tk.END, content)
        notebook.forget(notebook.select())
        notebook.add(note_content, text=title)
    
    save_edited_button = ttk.Button(note_frame, text="Save Edited Note",
                                command=save_edited_note, style="secondary.TButton")
    save_edited_button.grid(row=2, column=0, padx=10, pady=10)
    

edit_note_button = ttk.Button(root, text="Edit Note",
                    command=edit_note, style="dark.TButton")
edit_note_button.pack(side=tk.RIGHT, padx=10, pady=10)
    

#method to delete note
def delete_note():
    #get the current tab index
    current_tab = notebook.index(notebook.select())

    #get note title
    note_title = notebook.tab(current_tab, "text")

    #confirm deletion
    confirm = messagebox.askyesno("Delete note",
                                    f"Are you sure you want to delete {note_title}?")
    
    if confirm:
        #remove from notebook
        notebook.forget(current_tab)

        #remove from notes dictionary
        notes.pop(note_title)

        #save notes to file
        with open("app_notes.json","w") as f:
            json.dump(notes, f)


#Buttons

new_note_button = ttk.Button(root, text="New Note",
                    command=add_note, style="dark.TButton")
new_note_button.pack(side=tk.LEFT, padx=10, pady=10)

delete_note_button = ttk.Button(root, text="Delete Note",
                        command=delete_note, style="dark.TButton")
delete_note_button.pack(side=tk.LEFT, padx=10, pady=10)



root.mainloop()