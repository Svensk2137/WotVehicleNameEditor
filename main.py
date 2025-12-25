#!/usr/bin/python3.14
import tkinter as tk
from tkinter import filedialog


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wot Vehicle name changer")
        self.geometry("500x200")
        self.create_widgets()

        self.lcFolder = ""

    def create_widgets(self):
        filepickerbutton = tk.Button(self, text="Pick file", command=self.pickFolder)
        filepickerbutton.pack()
        self.pathLabel = tk.Label(
            self, text="Choose folder <WOT main dir>/res/text/lc_messages/"
        )
        self.pathLabel.pack()

    def pickFolder(self):
        lcfolder = filedialog.askdirectory(
            title="Select lc_messages folder",
            initialdir="/drives/Gaming/SteamLibrary/steamapps/common/World of Tanks/eu/res/text/",
        )
        self.pathLabel["text"] = lcfolder
        # wottext = polib.mofile(mofile)
        self.lcFolder = lcfolder


# vehicleName = input("Write the name of the vehicle: ")

# for entry in wottext:
#    if vehicleName in entry.msgid:
#        print(f'{entry.msgid}: "{entry.msgstr}"')
if __name__ == "__main__":
    app = App()
    app.mainloop()
