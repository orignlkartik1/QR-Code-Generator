import qrcode
from tkinter import *
from tkinter import messagebox, filedialog
from PIL import ImageTk

def generate_qr():
    data = entry.get().strip()
    if not data:
        messagebox.showwarning("Warning", "Please enter text or URL")
        return

    global qr_image, tk_qr_image
    qr_image = qrcode.make(data)
    tk_qr_image = ImageTk.PhotoImage(qr_image.resize((250,250)))

    qr_label.config(image=tk_qr_image)
    save_button.config(state=NORMAL)

def save_qr():
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG Files", "*.png")])
    if file_path:
        qr_image.save(file_path)
        messagebox.showinfo("Saved", "QR Code saved successfully!")

# GUI Window
root = Tk()
root.title("QR Code Generator")
root.geometry("400x500")
root.resizable(False, False)

Label(root, text="QR Code Generator", font=("Arial", 18, "bold")).pack(pady=10)
Label(root, text="Enter Text or URL:", font=("Arial", 12)).pack()

entry = Entry(root, font=("Arial", 12), width=40)
entry.pack(pady=10)

Button(root, text="Generate QR", font=("Arial", 12, "bold"), command=generate_qr).pack(pady=10)

qr_label = Label(root)
qr_label.pack()

save_button = Button(root, text="Save QR", font=("Arial", 12, "bold"),
                     state=DISABLED, command=save_qr)
save_button.pack(pady=10)

root.mainloop()
