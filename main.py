#!/usr/bin/python3.14
import os
import sys
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
        self.text_files = []
        for entry in os.listdir(self.lcfolder):
            if "_vehicles.mo" in entry:
                self.text_files.append(entry)

        print(self.text_files)
        if self.text_files == []:
            messagebox.showerror("Huh?", "Picked a wrong folder or canceled")
            sys.exit()

        self.option_var_nation = tk.StringVar(self)
        self.option_var_vehicle = tk.StringVar(self)
        self.create_widgets()

    def create_widgets(self):
        self.nation_options = ttk.OptionMenu(
            self,
            self.option_var_nation,
            self.text_files[0],
            *self.text_files,
            command=self.populate_vehicles,
        )
        self.nation_options.pack()

        self.vehicle_options = ttk.Combobox(
            self,
            textvariable=self.option_var_vehicle,
            state="readonly",
        )
        self.vehicle_options.pack()

        ttk.Button(self, text="Load Info", command=self.load_tank_name).pack()

        ttk.Label(self, text="Vehicle name").pack()
        self.tank_name = ttk.Entry(self)
        self.tank_name.pack()
        ttk.Label(self, text="Vehicle short name").pack()
        self.short_tank_name = ttk.Entry(self)
        self.short_tank_name.pack()

        ttk.Button(self, text="SAVE", width=10).pack()

    def populate_vehicles(self, *args):
        path = self.lcfolder + "/" + self.option_var_nation.get()
        self.currlist = polib.mofile(path)
        vehicles = []
        for entry in self.currlist:
            if "_descr" in entry.msgid:
                proper_id = entry.msgid.replace("_descr", "")
                vehicles.append(proper_id)
        self.vehicle_options["values"] = vehicles

    def load_tank_name(self, *args):
        selected_vehicle = self.option_var_vehicle.get()
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
            self.tank_name.delete(0, tk.END)
            self.tank_name.insert(0, str(veh_name))
            print(f"Short: {short_name}")
            self.short_tank_name.delete(0, tk.END)
            self.short_tank_name.insert(0, str(short_name))


if __name__ == "__main__":
    app = App()
    app.mainloop()
