import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from rename_tool.tool.rename_class import ReName
import os


# Define the GUI class
class GUI:
    # Initialize variables
    initial_dir = "/"
    picked_season = 0
    picked_path = ""
    season_paths = {}
    history = []

    # Create a dictionary for seasons
    for x in range(1, 26):
        season_paths[x] = []

    # Define a method to clear the variables
    def clear(self):
        self.picked_season = 0
        self.picked_path = ""
        self.history = []
        self.season_paths = {}
        for x in range(1, 26):
            self.season_paths[x] = []
        self.update_label()
        self.path_label.config(text=self.picked_path)
        self.dropdown.config(textvariable=self.variable, values=self.options)
        self.message("")

    # Define a method to show the dictionary
    def show_dict(self):
        text = ""
        for index in self.season_paths:
            text += f"Season {index:02d}:"
            for path in self.season_paths[index]:
                text += f" {os.path.basename(path)};"
            if len(self.season_paths[index]) == 0:
                text += " --- "
            text += "\n"
        return text

    # Define a method to open the file explorer
    def open_file_explorer(self):
        self.picked_path = filedialog.askdirectory(initialdir=self.initial_dir)
        self.path_label.config(text=self.picked_path)

    # Define a method to update the label
    def update_label(self):
        self.label.config(text=self.show_dict())

    def message(self, text):
        self.msg_label.config(text=text)

    # Define a method to add a season
    def add(self):

        if os.path.isdir(self.picked_path) and self.picked_season > 0:    # nopep8
            for entry_list in self.season_paths.values():
                if self.picked_path in entry_list:
                    self.message("Path already added!")
                    return

            self.message("")
            self.season_paths[self.picked_season].append(self.picked_path)
            self.history.append(self.picked_path)
            self.initial_dir = os.path.dirname(self.picked_path)
            self.update_label()
            self.picked_path = ""
            self.path_label.config(text=self.picked_path)

        else:
            self.message("Please enter a valid path and Season!")

    # Define a method to change the option
    def option_changed(self, *args):
        if self.variable.get().isnumeric():
            self.picked_season = int(self.variable.get())
        self.update_label()

    # Define a method to send the changes
    def send(self):
        rename = ReName(self.season_paths)
        success = rename.rename_files()
        self.message(success)

    def go_back(self):
        if len(self.history) >= 1:
            for season_index in self.season_paths.keys():
                for path in self.season_paths[season_index]:
                    if path == self.history[-1]:
                        self.picked_path = path
                        self.path_label.config(text=self.picked_path)
                        self.season_paths[season_index].remove(path)
                        self.history.remove(path)

            self.update_label()

    # Define the constructor for the GUI class
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1000x500")
        self.root.title("Rename")

        self.options = ["---"] + list(self.season_paths.keys())
        self.variable = tk.StringVar(self.root)
        self.variable.set(self.options[0])
        self.variable.trace("w", self.option_changed)
        self.dropdown = ttk.Combobox(self.root, textvariable=self.variable, values=self.options)

        self.label = tk.Label(self.root, text=self.show_dict(), justify="left")
        self.path_label = tk.Label(self.root, text=self.picked_path)
        self.msg_label = tk.Label(self.root, text="")

        self.button = tk.Button(self.root, text="File ...", command=self.open_file_explorer)
        self.exit_button = tk.Button(self.root, text="Close", command=self.root.destroy)
        self.clear_button = tk.Button(self.root, text="Reset", command=self.clear)
        self.send_button = tk.Button(self.root, text="Run!", command=self.send)
        self.add_button = tk.Button(self.root, text="Add", command=self.add)
        self.back_button = tk.Button(self.root, text="<-", command=self.go_back)

        self.button.place(x=20, y=40)
        self.exit_button.place(x=850, y=40)
        self.clear_button.place(x=780, y=40)
        self.send_button.place(x=710, y=40)
        self.back_button.place(x=640, y=40)

        self.add_button.place(x=380, y=40)
        self.dropdown.place(x=200, y=40)
        self.label.place(x=20, y=150)
        self.path_label.place(x=20, y=80)
        self.msg_label.place(x=20, y=120)

        self.root.mainloop()


# Create an instance of the GUI class
win = GUI()


