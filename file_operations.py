import os
import xml.etree.ElementTree as ET
from tkinter import messagebox
import traceback

def modify_xml_attribute(selected_names, file_path, output_dir):
    try:
        os.makedirs(output_dir, exist_ok=True)

        created_files = []

        for name in selected_names:
            # Load and parse the XML file
            tree = ET.parse(file_path)
            root_element = tree.getroot()

            # Find <cycle> element with name="EXTRASUNNY" and regions="2"
            for cycle in root_element.findall(".//cycle[@name='EXTRASUNNY'][@regions='2']"):
                # Change the value of the name attribute
                cycle.set("name", name)
                break
            else:
                messagebox.showerror("Error", f"<cycle> element with attributes name='EXTRASUNNY' and regions='2' not found in file {name}.xml!")
                continue

            # Form the name of the new file based on the selected value
            file_name = f"{name_to_filename[name]}.xml"  # Ensure filename format is correct
            save_path = os.path.join(output_dir, file_name)

            if os.path.isfile(save_path):
                # Prompt user to replace the existing file
                response = messagebox.askyesno("File Exists", f"The file {file_name} already exists. Do you want to replace it?")
                if not response:
                    continue  # Skip file creation if the user does not want to replace the existing file

            # Save the modified XML file
            tree.write(save_path, encoding="utf-8", xml_declaration=True)
            created_files.append(file_name)  # Add only the file name to the list

        if created_files:
            # Message about the created files
            messagebox.showinfo("Success", f"Files successfully created in the folder:\n{output_dir}\n\nList of created files:\n" + "\n".join(created_files))
                
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        print("Error:", traceback.format_exc())
        input("Press Enter to close...")

# Ensure this dictionary is available for use in the function
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
