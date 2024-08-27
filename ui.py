import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from file_operations import modify_xml_attribute

class XMLModifierUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Modify XML Attribute")
        self.root.geometry("400x500")

        self.selected_file_path = None

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.checkboxes = {}

        self.create_file_selection_frame()
        self.create_checkbox_frames()
        self.create_save_button()

    def create_file_selection_frame(self):
        file_selection_frame = ctk.CTkFrame(self.root)
        file_selection_frame.pack(pady=10, padx=10, fill="x")

        file_select_button = ctk.CTkButton(file_selection_frame, text="Select XML File", command=self.on_file_select)
        file_select_button.pack(side="left")

        self.file_name_label = ctk.CTkLabel(file_selection_frame, text="No file selected")
        self.file_name_label.pack(side="left", padx=10)

    def create_checkbox_frames(self):
        self.regular_frame = ctk.CTkFrame(self.root)
        self.regular_frame.pack(pady=5, padx=10, fill="x")

        self.rain_thunder_frame = ctk.CTkFrame(self.root)
        self.rain_thunder_frame.pack(pady=5, padx=10, fill="x")

        self.snowlight_xmas_halloween_frame = ctk.CTkFrame(self.root)
        self.snowlight_xmas_halloween_frame.pack(pady=5, padx=10, fill="x")

        self.create_checkboxes()

    def create_checkboxes(self):
        name_to_filename = {
            "BLIZZARD": "w_blizzard",
            "CLEAR": "w_clear",
            "CLEARING": "w_clearing",
            "CLOUDS": "w_clouds",
            "EXTRASUNNY": "w_extrasunny",
            "FOGGY": "w_foggy",
            "NEUTRAL": "w_neutral",
            "OVERCAST": "w_overcast",
            "RAIN": "w_rain",
            "SMOG": "w_smog",
            "SNOW": "w_snow",
            "THUNDER": "w_thunder",
            "SNOWLIGHT": "w_snowlight",
            "XMAS": "w_xmas",
            "HALLOWEEN": "w_halloween"
        }

        def create_checkbox(parent, text, variable):
            checkbox = ctk.CTkCheckBox(parent, text=text, variable=variable,
                                       corner_radius=8, 
                                       width=20, 
                                       height=20,
                                       border_width=2, 
                                       border_color="gray",
                                       text_color="white",
                                       state="disabled")
            checkbox.pack(anchor='w')
            return checkbox

        for name in name_to_filename.keys():
            var = ctk.BooleanVar()
            if name in ["RAIN", "THUNDER"]:
                checkbox = create_checkbox(self.rain_thunder_frame, name, var)
            elif name in ["SNOWLIGHT", "XMAS", "HALLOWEEN"]:
                checkbox = create_checkbox(self.snowlight_xmas_halloween_frame, name, var)
            else:
                checkbox = create_checkbox(self.regular_frame, name, var)
            self.checkboxes[name] = checkbox

    def create_save_button(self):
        self.save_button = ctk.CTkButton(self.root, text="Create New Timecycle", command=self.on_checkbox_click, state="disabled")
        self.save_button.pack(pady=10)

    def on_file_select(self):
        file_path = filedialog.askopenfilename(title="Select XML File", filetypes=[("XML Files", "*.xml")])
        if file_path:
            self.file_name_label.configure(text=os.path.basename(file_path))
            self.save_button.configure(state="normal")
            self.selected_file_path = file_path

            for checkbox in self.checkboxes.values():
                checkbox.configure(state="normal")

    def on_checkbox_click(self):
        selected_names = [name for name, var in self.checkboxes.items() if var.get()]
        if selected_names:
            if self.selected_file_path:
                output_dir = filedialog.askdirectory(title="Select Folder for Saving Files")
                if output_dir:
                    modify_xml_attribute(selected_names, self.selected_file_path, output_dir)
                    for var in self.checkboxes.values():
                        var.deselect()
                    self.save_button.configure(state="disabled")
                    self.file_name_label.configure(text="No file selected")
                    self.selected_file_path = None
            else:
                messagebox.showerror("Error", "No file selected!")
        else:
            messagebox.showwarning("Warning", "Select at least one value for the name attribute!")
