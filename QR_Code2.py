import qrcode
from tkinter import *
from tkinter import messagebox, filedialog, colorchooser
from PIL import Image, ImageTk

fg_color = "black"
bg_color = "white"
qr_image = None
logo_path = None

def choose_fg_color():
    global fg_color
    color = colorchooser.askcolor(title="Foreground Color")[1]
    if color:
        fg_color = color
        fg_btn.config(bg=color)

def choose_bg_color():
    global bg_color
    color = colorchooser.askcolor(title="Background Color")[1]
    if color:
        bg_color = color
        bg_btn.config(bg=color)

def select_logo():
    global logo_path
    logo_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if logo_path:
        logo_btn.config(text="Logo Selected ✅")

def generate_qr():
    global qr_image, tk_qr_image

    data = entry.get().strip()
    if not data:
        messagebox.showwarning("Warning", "Please enter text or URL")
        return

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color=fg_color, back_color=bg_color).convert("RGB")

    # Insert Logo if selected
    if logo_path:
        try:
            logo = Image.open(logo_path)
            logo = logo.convert("RGBA")

            # Resize logo relative to QR size
            qr_size = qr_img.size[0]
            logo_size = qr_size // 4
            logo = logo.resize((logo_size, logo_size))

            # Center position
            x = (qr_size - logo_size) // 2
            y = (qr_size - logo_size) // 2

            qr_img.paste(logo, (x, y), logo)
        except Exception as e:
            messagebox.showerror("Error", f"Logo could not be added\n{e}")

    qr_image = qr_img
    tk_qr_image = ImageTk.PhotoImage(qr_img.resize((250, 250)))

    qr_label.config(image=tk_qr_image)
    save_btn.config(state=NORMAL)

def save_qr():
    if qr_image is None:
        return

    file = filedialog.asksaveasfilename(defaultextension=".png",
                                        filetypes=[("PNG Files", "*.png")])
    if file:
        qr_image.save(file)
        messagebox.showinfo("Saved", "QR Code Saved Successfully ✅")

# UI Window
root = Tk()
root.title("QR Code Generator")
root.geometry("450x600")
root.resizable(False, False)

Label(root, text="QR Code Generator", font=("Arial", 18, "bold")).pack(pady=10)

Label(root, text="Enter Text / URL:", font=("Arial", 12)).pack()
entry = Entry(root, font=("Arial", 12), width=40)
entry.pack(pady=8)

# Color selection buttons
color_frame = Frame(root)
color_frame.pack(pady=8)

fg_btn = Button(color_frame, text="Foreground", width=15, bg="black", fg="white",
                command=choose_fg_color)
fg_btn.grid(row=0, column=0, padx=5)

bg_btn = Button(color_frame, text="Background", width=15, bg="white",
                command=choose_bg_color)
bg_btn.grid(row=0, column=1, padx=5)

# Logo button
logo_btn = Button(root, text="Add Center Logo", font=("Arial", 10), command=select_logo)
logo_btn.pack(pady=5)

Button(root, text="Generate QR Code", font=("Arial", 12, "bold"),
       command=generate_qr).pack(pady=10)

qr_label = Label(root)
qr_label.pack(pady=10)

save_btn = Button(root, text="Save QR", font=("Arial", 12, "bold"),
                  state=DISABLED, command=save_qr)
save_btn.pack(pady=10)

root.mainloop()
