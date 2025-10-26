
import qrcode
from tkinter import *
from tkinter import messagebox, filedialog, colorchooser
from PIL import Image, ImageTk

fg_color = "black"
bg_color = "white"
qr_image = None
tk_qr_image = None

def choose_fg_color():
    global fg_color
    color = colorchooser.askcolor(title="Choose Foreground Color")[1]
    if color:
        fg_color = color
        fg_btn.config(bg=color)

def choose_bg_color():
    global bg_color
    color = colorchooser.askcolor(title="Choose Background Color")[1]
    if color:
        bg_color = color
        bg_btn.config(bg=color)

def generate_qr():
    data = entry.get().strip()
    if not data:
        messagebox.showwarning("Warning", "Please enter text or URL")
        return

    global qr_image, tk_qr_image
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    qr_image = qr.make_image(fill_color=fg_color, back_color=bg_color)
    tk_qr_image = ImageTk.PhotoImage(qr_image.resize((250,250)))

    qr_label.config(image=tk_qr_image)
    save_button.config(state=NORMAL)

def save_qr():
    if qr_image is None:
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG Files", "*.png")])
    if file_path:
        qr_image.save(file_path)
        messagebox.showinfo("Saved", "QR Code saved successfully!")

# GUI
root = Tk()
root.title("QR Code Generator")
root.geometry("420x550")
root.resizable(False, False)

Label(root, text="QR Code Generator", font=("Arial", 18, "bold")).pack(pady=10)
Label(root, text="Enter Text or URL:", font=("Arial", 12)).pack()

entry = Entry(root, font=("Arial", 12), width=40)
entry.pack(pady=10)

# Color Selection Buttons
color_frame = Frame(root)
color_frame.pack(pady=10)

fg_btn = Button(color_frame, text="Foreground Color", font=("Arial", 10),
                width=18, command=choose_fg_color, bg="black", fg="white")
fg_btn.grid(row=0, column=0, padx=5)

bg_btn = Button(color_frame, text="Background Color", font=("Arial", 10),
                width=18, command=choose_bg_color, bg="white", fg="black")
bg_btn.grid(row=0, column=1, padx=5)

Button(root, text="Generate QR", font=("Arial", 12, "bold"),
       command=generate_qr).pack(pady=10)

qr_label = Label(root)
qr_label.pack(pady=10)

save_button = Button(root, text="Save QR", font=("Arial", 12, "bold"),
                     state=DISABLED, command=save_qr)
save_button.pack(pady=10)

root.mainloop()
