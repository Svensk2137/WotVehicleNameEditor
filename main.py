#!/usr/bin/python3.14
import os
import tkinter as tk
from pydoc import text
from tkinter import filedialog, messagebox, ttk

import polib


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wot Vehicle name changer")
        self.geometry("500x300")

        self.excluded_strings = [
            "Chassis_",
            "Turret_",
            "_descr",
            "_long_special",
            "_short",
            "_short_special",
        ]

        print("Ask for lc_messages folder")
        self.lcfolder = filedialog.askdirectory(
            title="Select lc_messages folder",
            initialdir="/drives/Gaming/SteamLibrary/steamapps/common/World of Tanks/eu/res/text/",
        )

        print("Get *_vehicles.mo files")
        self.textFiles = []
        for entry in os.listdir(self.lcfolder):
            if "_vehicles.mo" in entry:
                self.textFiles.append(entry)

        print(self.textFiles)
        if self.textFiles == []:
            messagebox.showerror("Huh?", "Picked a wrong folder or canceled")
            exit()

        self.optionVarNation = tk.StringVar(self)
        self.create_widgets()

    def create_widgets(self):
        self.nationOptions = ttk.OptionMenu(
            self,
            self.optionVarNation,
            self.textFiles[0],
            *self.textFiles,
            command=self.populateVehicles,
        )
        self.nationOptions.pack()

        self.vehicleOptions = ttk.OptionMenu(self, self.optionVarNation, "")
        self.vehicleOptions.pack()

        ttk.Label(self, text="Vehicle name").pack()
        self.tankName = ttk.Entry(self)
        self.tankName.pack()

    def populateVehicles(self, *args):
        menu = self.vehicleOptions["menu"]
        menu.delete(0, "end")
        path = self.lcfolder + "/" + self.optionVarNation.get()
        print(path)
        list = polib.mofile(path)
        vehicles = []
        for entry in list:
            if entry.msgid and not any(
                excluded in entry.msgid for excluded in self.excluded_strings
            ):
                print(entry)
                vehicles.append(entry.msgid)
        print(vehicles)


# vehicleName = input("Write the name of the vehicle: ")

# for entry in wottext:
#    if vehicleName in entry.msgid:
#        print(f'{entry.msgid}: "{entry.msgstr}"')
if __name__ == "__main__":
    app = App()
    app.mainloop()
