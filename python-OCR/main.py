import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont
import pytesseract

pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        global img, text_data
        img = Image.open(file_path)
        text_data = pytesseract.image_to_data(
            img, output_type=pytesseract.Output.DICT, config="--psm 6"
        )
        display_text()

def display_text():
    text_widget.delete("1.0", tk.END)
    for i, word in enumerate(text_data['text']):
        if word.strip():
            x, y, w, h = (text_data['left'][i], text_data['top'][i],
                          text_data['width'][i], text_data['height'][i])
            line = f"{i}: ({x}, {y}, {w}, {h}) - {word}\n"
            text_widget.insert(tk.END, line)

def save_image():
    edited_text = text_widget.get("1.0", tk.END).splitlines()
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 14) 

    for line in edited_text:
        if line.strip():
            idx, word = line.split(" - ")
            i = int(idx.split(":")[0])
            x, y = text_data['left'][i], text_data['top'][i]
            draw.text((x, y), word.strip(), font=font, fill="black")

    img.save("edited_report.jpg")
    print("Edited report saved as 'edited_report.jpg'")


root = tk.Tk()
root.title("Report Editor")

upload_btn = tk.Button(root, text="Upload Image", command=upload_image)
upload_btn.pack()

text_widget = tk.Text(root, height=20, width=80)
text_widget.pack()

save_btn = tk.Button(root, text="Save Edited Report", command=save_image)
save_btn.pack()

root.mainloop()
