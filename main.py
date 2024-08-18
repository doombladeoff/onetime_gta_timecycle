import xml.etree.ElementTree as ET
from tkinter import Tk, filedialog, messagebox, BooleanVar, Checkbutton, Button, Label
import os
import traceback

# Словарь для сопоставления значений чекбоксов и имен файлов
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
    "SNOW": "w_snow"
}

def modify_xml_attribute(selected_names, file_path, output_dir):
    try:
        os.makedirs(output_dir, exist_ok=True)

        created_files = []

        for name in selected_names:
            # Загружаем и парсим XML файл
            tree = ET.parse(file_path)
            root_element = tree.getroot()

            # Ищем элемент <cycle> с атрибутами name="EXTRASUNNY" и regions="2"
            for cycle in root_element.findall(".//cycle[@name='EXTRASUNNY'][@regions='2']"):
                # Меняем значение атрибута name
                cycle.set("name", name)
                break
            else:
                messagebox.showerror("Ошибка", f"Элемент <cycle> с атрибутами name='EXTRASUNNY' и regions='2' не найден в файле {name_to_filename[name]}.xml!")
                continue

            # Формируем имя нового файла на основе выбранного значения
            new_file_name = f"{name_to_filename[name]}.xml"
            save_path = os.path.join(output_dir, new_file_name)

            # Сохраняем измененный XML файл
            tree.write(save_path, encoding="utf-8", xml_declaration=True)
            created_files.append(new_file_name)  # Добавляем только имя файла

        if created_files:
            # Сообщение о создании всех файлов
            messagebox.showinfo("Успех", f"Файлы успешно созданы в папке:\n{output_dir}\n\nСписок созданных файлов:\n" + "\n".join(created_files))
                
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
        print("Ошибка:", traceback.format_exc())
        input("Нажмите Enter, чтобы закрыть...")

def on_checkbox_click():
    selected_names = [name for name, var in checkboxes.items() if var.get()]
    if selected_names:
        # Открываем диалоговое окно для выбора XML файла
        file_path = filedialog.askopenfilename(title="Выберите XML файл", filetypes=[("XML Files", "*.xml")])

        if file_path:
            # Открываем диалоговое окно для выбора папки для сохранения файлов
            output_dir = filedialog.askdirectory(title="Выберите папку для сохранения файлов")
            
            if output_dir:
                modify_xml_attribute(selected_names, file_path, output_dir)
            else:
                messagebox.showerror("Ошибка", "Папка для сохранения файлов не выбрана!")
        else:
            messagebox.showerror("Ошибка", "Файл не выбран!")
    else:
        messagebox.showwarning("Внимание", "Выберите хотя бы одно значение для атрибута name!")

# Создаем главное окно
root = Tk()
root.title("Изменение XML атрибута")

# Создаем словарь для хранения состояний чекбоксов
checkboxes = {}

# Добавляем метку с инструкцией
label = Label(root, text="Выберите значения для атрибута name:")
label.pack(pady=5)

# Создаем чекбоксы для каждого значения
for name in name_to_filename.keys():
    var = BooleanVar()
    checkbutton = Checkbutton(root, text=name, variable=var)
    checkbutton.pack(anchor='w')
    checkboxes[name] = var

# Добавляем кнопку для сохранения изменений
save_button = Button(root, text="Выбрать файл и создать новые", command=on_checkbox_click)
save_button.pack(pady=10)

# Запускаем главный цикл приложения
root.mainloop()
