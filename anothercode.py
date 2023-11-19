import cv2
import os
import string
import tkinter as tk
from tkinter import filedialog

# Create a root window
root = tk.Tk()
root.title("Image Steganography")

# Define global variables
image_path = None
img = None
msg = None
password = None
d = {}
c = {}

# Populate dictionaries for character to integer and vice versa
for i in range(256):
    d[chr(i)] = i
    c[i] = chr(i)

# Define functions for encryption and decryption
def encrypt():
    global image_path, img, msg, password
    # Get the image path from the file dialog
    image_path = filedialog.askopenfilename()
    # Load the image
    img = cv2.imread(image_path)
    # Check if the image is valid
    if img is None:
        tk.messagebox.showerror("Error", f"Unable to load image from {image_path}. Please check the file path.")
        return
    # Get the secret message from the entry box
    msg = msg_entry.get()
    # Get the password from the entry box
    password = password_entry.get()
    # Initialize the indices for the image pixels
    n = 0
    m = 0
    z = 0
    # Loop through the message characters and hide them in the image pixels
    for i in range(len(msg)):
        img[n, m, z] = d[msg[i]]
        n = n + 1
        m = m + 1
        z = (z + 1) % 3
        if n == img.shape[0] or m == img.shape[1] or z == img.shape[2]:
            break
    # Save the encrypted image as a new file
    cv2.imwrite("Encryptedmsg.jpg", img)
    # Show a success message
    tk.messagebox.showinfo("Success", "The image has been encrypted and saved as Encryptedmsg.jpg")
    # Open the encrypted image
    os.system("start Encryptedmsg.jpg")

def decrypt():
    global image_path, img, msg, password
    # Get the password from the entry box
    pas = password_entry.get()
    # Check if the password matches the original one
    if password == pas:
        # Initialize the indices for the image pixels
        n = 0
        m = 0
        z = 0
        # Initialize the decrypted message
        message = ""
        # Loop through the message characters and retrieve them from the image pixels
        for i in range(len(msg)):
            message = message + c[img[n, m, z]]
            n = n + 1
            m = m + 1
            z = (z + 1) % 3
            if n == img.shape[0] or m == img.shape[1] or z == img.shape[2]:
                break
        # Show the decrypted message
        tk.messagebox.showinfo("Decryption message", message)
    else:
        # Show an error message
        tk.messagebox.showerror("Error", "Not a valid key.")

# Create labels and entry boxes for the message and password
msg_label = tk.Label(root, text="Enter secret message:")
msg_label.grid(row=0, column=0, padx=10, pady=10)
msg_entry = tk.Entry(root)
msg_entry.grid(row=0, column=1, padx=10, pady=10)
password_label = tk.Label(root, text="Enter password:")
password_label.grid(row=1, column=0, padx=10, pady=10)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

# Create buttons for encryption and decryption
encrypt_button = tk.Button(root, text="Encrypt", command=encrypt)
encrypt_button.grid(row=2, column=0, padx=10, pady=10)
decrypt_button = tk.Button(root, text="Decrypt", command=decrypt)
decrypt_button.grid(row=2, column=1, padx=10, pady=10)

# Start the main loop
root.mainloop()
