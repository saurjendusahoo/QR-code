import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode
from PIL import Image, ImageTk

def generate_qr_code():
    """
    Gets the URL from the entry box, generates the QR code,
    displays it in the GUI, and asks the user where to save it.
    """
    url = url_entry.get()

    if not url:
        messagebox.showerror("Error", "Please enter a URL first.")
        return

    try:
        # --- Generate the QR Code ---
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Create the QR image using PIL (Pillow)
        img = qr.make_image(fill_color="black", back_color="white")

        # --- Display the image in the Tkinter window ---
        # Resize the image for a consistent preview size
        img_preview = img.resize((250, 250), Image.LANCZOS)
        
        # Convert PIL image to a Tkinter-compatible photo image
        tk_image = ImageTk.PhotoImage(img_preview)

        # Update the image label
        image_label.config(image=tk_image)
        # IMPORTANT: Keep a reference to the image to prevent it
        # from being garbage-collected by Python
        image_label.image = tk_image

        # --- Ask the user where to save the file ---
        # Open a "Save As..." dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            initialfile="my_qr_code.png"
        )

        # If the user selected a path (didn't click cancel)
        if file_path:
            # Save the *original* high-quality image, not the preview
            img.save(file_path)
            status_label.config(text=f"Saved to: {file_path}", fg="green")
        else:
            status_label.config(text="Save cancelled.", fg="orange")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        status_label.config(text="Generation failed.", fg="red")


# --- Set up the main application window ---
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("400x450")
root.resizable(False, False) # Prevent resizing

# Use a theme-aware frame for better styling
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(expand=True, fill="both")

# --- Create the GUI widgets ---

# 1. URL Label and Entry
url_label = ttk.Label(main_frame, text="Enter Website URL:")
url_label.pack(pady=5)

url_entry = ttk.Entry(main_frame, width=50)
url_entry.pack(pady=5, padx=10)
url_entry.insert(0, "")

# 2. Generate Button
generate_button = ttk.Button(
    main_frame,
    text="Generate & Save QR Code",
    command=generate_qr_code
)
generate_button.pack(pady=10)

# 3. Image Preview Label (will be empty at first)
image_label = ttk.Label(main_frame)
image_label.pack(pady=10)

# 4. Status Label
status_label = ttk.Label(main_frame, text="")
status_label.pack(pady=5)

# --- Start the application ---
root.mainloop()