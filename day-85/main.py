import tkinter as tk 
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont


GREEN = "#9bdeac"
RED = "#e7305b"

url = ""

def on_entry_click(event):
    """Borra el placeholder cuando el usuario hace clic en el Entry."""
    if entry.get() == placeholder:
        entry.delete(0, tk.END)
        entry.config(fg="black")  # Cambia el color del texto a negro

def on_focus_out(event):
    """Si el Entry está vacío al perder el foco, vuelve a mostrar el placeholder."""
    if entry.get() == "":
        entry.insert(0, placeholder)
        entry.config(fg="gray")


def done():
    global url
    if not url:
        print("No image selected.")
        return

    watermark_text = entry.get()
    if watermark_text == placeholder or watermark_text.strip() == "":
        print("No valid watermark text entered.")
        return
    try:
        image = Image.open(url)
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype("arial.ttf", 200) 
        except IOError:
            font = ImageFont.load_default() 

        width, height = image.size
        text_width, text_height = draw.textsize(watermark_text, font=font)
        position = (width/2 - text_width - 10, height/2 - text_height - 10)

        draw.text(position, watermark_text, fill=(255, 255, 255, 128), font=font)  # White semi-transparent

        new_path = url.replace(".", "_watermarked.")
        image.save(new_path)
        print(f"Watermarked image saved at: {new_path}")

    except Exception as e:
        print("Error processing the image:", e)

def select(): 
    global url
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*")])
    url = archivo
    print(url)    





window = tk.Tk()
window.title("Watermark")
window.config(padx=100, pady=50, bg=GREEN)
window.resizable(False, False)


label = tk.Label(text="Choose an image", font = ('Courier', 15, 'bold'), bg=GREEN)
label.grid(row = 0, column=0)

select
button = tk.Button(window, text = "Choose", font = ('Courier', 15, 'bold'), command=select)
button.grid(row = 1, column=0)

placeholder = "Write your watermark..."

entry = tk.Entry(window, width=20)
entry.insert(0, placeholder)  
entry.bind("<FocusIn>", on_entry_click)
entry.bind("<FocusOut>", on_focus_out)
entry.grid(row = 0, column=2, padx=100)

doneBtn = tk.Button(window, text = "Done", font = ('Courier', 15, 'bold'), command=done)
doneBtn.grid(row = 1, column=2, padx=50, pady=100)


window.mainloop()
