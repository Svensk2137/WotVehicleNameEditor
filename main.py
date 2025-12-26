#!/usr/bin/python3.14
"""
We moding some shit :DDDDDDD
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import polib


class App(tk.Tk):
    """
    Idk, main class or sumthin, here is your docstring pylint
    """

    def __init__(self):
        super().__init__()
        self.title("Wot Vehicle name changer")
        self.geometry("250x300")
        self.resizable(False, False)

        print("Ask for lc_messages folder")
        self.lcfolder = filedialog.askdirectory(
            title="Select lc_messages folder",
            initialdir="/drives/Gaming/SteamLibrary/steamapps/common/World of Tanks/eu/res_mods/2.1.0.2/text/lc_messages/",
        )

        print("Get *_vehicles.mo files")
        self.text_files = []
        for entry in os.listdir(self.lcfolder):
            if "_vehicles.mo" in entry:
                self.text_files.append(entry)

        print(self.text_files)
        if not self.text_files:
            messagebox.showerror("Huh?", "Picked a wrong folder or canceled")
            sys.exit()

        self.option_var_nation = tk.StringVar(self)
        self.option_var_vehicle = tk.StringVar(self)
        self.curr_list = None
        self.create_widgets()

    def create_widgets(self):
        """
        Load them widgets :)))
        """
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

        ttk.Button(self, text="SAVE", width=10, command=self.save_changes).pack()

        ttk.Label(
            self,
            text="If you dont want to modify oryginal\nfiles, copy the <nation>_vehicles.mo\nfile into\nres_mods/<version>/text/lc_messages/",
        ).pack()

    def populate_vehicles(self, *args):
        """
        you can read i think
        """
        path = self.lcfolder + "/" + self.option_var_nation.get()
        self.curr_list = polib.mofile(path)
        vehicles = []
        for entry in self.curr_list:
            if "_descr" in entry.msgid:
                proper_id = entry.msgid.replace("_descr", "")
                vehicles.append(proper_id)
        self.vehicle_options["values"] = vehicles

    def load_tank_name(self):
        """
        all of this a for better pylint score, why do i care?
        """
        if self.curr_list is None:
            messagebox.showwarning("Warning", "Please select a nation first")
            return
        selected_vehicle = self.option_var_vehicle.get()
        if selected_vehicle:
            veh_name = None
            short_name = None
            for entry in self.curr_list:
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

    def save_changes(self):
        """
        Save changes to the selected vehicle's name and short name in the .mo file
        """
        if self.curr_list is None:
            messagebox.showwarning("Bruh", "Select Nation")
            return

        selected_vehicle = self.option_var_vehicle.get()
        if not selected_vehicle:
            messagebox.showwarning("huh", "Select Vehicle")
            return

        new_name = self.tank_name.get()
        new_short_name = self.short_tank_name.get()

        found_name = False
        found_short = False
        for entry in self.curr_list:
            if entry.msgid == selected_vehicle:
                entry.msgstr = new_name
                found_name = True
            if entry.msgid == f"{selected_vehicle}_short":
                entry.msgstr = new_short_name
                found_short = True
            if found_name and found_short:
                break

        file_path = self.lcfolder + "/" + self.option_var_nation.get()
        self.curr_list.save(file_path)

        messagebox.showinfo("Success", f"Updated '{selected_vehicle}' name")


if __name__ == "__main__":
    app = App()
    app.mainloop()
