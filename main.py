#!/usr/bin/python3.14
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import polib


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wot Vehicle name changer")
        self.geometry("225x250")

        print("Ask for lc_messages folder")
        self.lcfolder = filedialog.askdirectory(
            title="Select lc_messages folder",
            initialdir="/drives/Gaming/SteamLibrary/steamapps/common/World of Tanks/eu/res/text/lc_messages",
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
        self.optionVarVehicle = tk.StringVar(self)
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

        self.vehicleOptions = ttk.Combobox(
            self,
            textvariable=self.optionVarVehicle,
            state="readonly",
        )
        self.vehicleOptions.pack()

        ttk.Button(self, text="Load Info", command=self.loadTankName).pack()

        ttk.Label(self, text="Vehicle name").pack()
        self.tankName = ttk.Entry(self)
        self.tankName.pack()
        ttk.Label(self, text="Vehicle short name").pack()
        self.shortTankName = ttk.Entry(self)
        self.shortTankName.pack()

        ttk.Button(self, text="SAVE", width=10).pack()

    def populateVehicles(self, *args):
        path = self.lcfolder + "/" + self.optionVarNation.get()
        self.currlist = polib.mofile(path)
        vehicles = []
        for entry in self.currlist:
            if "_descr" in entry.msgid:
                properID = entry.msgid.replace("_descr", "")
                vehicles.append(properID)
        self.vehicleOptions["values"] = vehicles

    def loadTankName(self, *args):
        selected_vehicle = self.optionVarVehicle.get()
        if selected_vehicle:
            veh_name = None
            short_name = None
            for entry in self.currlist:
                if entry.msgid == f"{selected_vehicle}":
                    veh_name = entry.msgstr
                elif entry.msgid == f"{selected_vehicle}_short":
                    short_name = entry.msgstr
                if veh_name and short_name:
                    break
            print(f"Vehicle: {selected_vehicle}")
            print(f"Name: {veh_name}")
            self.tankName.delete(0, tk.END)
            self.tankName.insert(0, str(veh_name))
            print(f"Short: {short_name}")
            self.shortTankName.delete(0, tk.END)
            self.shortTankName.insert(0, str(short_name))


if __name__ == "__main__":
    app = App()
    app.mainloop()
