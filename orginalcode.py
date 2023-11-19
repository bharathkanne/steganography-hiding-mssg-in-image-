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

# Function to upload and preview image
def upload_image():
    global image_path, img
    # Get the image path from the file dialog
    image_path = filedialog.askopenfilename()
    # Load the image
    img = cv2.imread(image_path)
    # Check if the image is valid
    if img is None:
        tk.messagebox.showerror("Error", f"Unable to load image from {image_path}. Please check the file path.")
        return
    # Display the image in a new window
    cv2.imshow("Preview Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Create frames for encryption and decryption
encryption_frame = tk.Frame(root)
encryption_frame.grid(row=0, column=0, padx=10, pady=10)

decryption_frame = tk.Frame(root)
decryption_frame.grid(row=0, column=1, padx=10, pady=10)

# Encryption functions
def encrypt():
    global image_path, img, msg, password
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

# Decryption function
def decrypt():
    global image_path, img, msg, password
    # Get the password from the entry box
    pas = decryption_password_entry.get()
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
        decryption_result_label.config(text="Decrypted Message: " + message)
    else:
        # Show an error message
        tk.messagebox.showerror("Error", "Not a valid key.")

# Create labels and entry boxes for the message and password in the encryption frame
msg_label = tk.Label(encryption_frame, text="Enter secret message:")
msg_label.grid(row=0, column=0, padx=10, pady=10)
msg_entry = tk.Entry(encryption_frame)
msg_entry.grid(row=0, column=1, padx=10, pady=10)

password_label = tk.Label(encryption_frame, text="Enter password:")
password_label.grid(row=1, column=0, padx=10, pady=10)
password_entry = tk.Entry(encryption_frame, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

upload_button = tk.Button(encryption_frame, text="Upload Image", command=upload_image)
upload_button.grid(row=2, column=0, columnspan=2, pady=10)

encrypt_button = tk.Button(encryption_frame, text="Encrypt", command=encrypt)
encrypt_button.grid(row=3, column=0, columnspan=2, pady=10)

# Create labels, entry boxes, and a button for decryption in the decryption frame
decryption_password_label = tk.Label(decryption_frame, text="Enter password:")
decryption_password_label.grid(row=0, column=0, padx=10, pady=10)
decryption_password_entry = tk.Entry(decryption_frame, show="*")
decryption_password_entry.grid(row=0, column=1, padx=10, pady=10)

decrypt_button = tk.Button(decryption_frame, text="Decrypt", command=decrypt)
decrypt_button.grid(row=1, column=0, columnspan=2, pady=10)

decryption_result_label = tk.Label(decryption_frame, text="Decrypted Message: ")
decryption_result_label.grid(row=2, column=0, columnspan=2, pady=10)

# Start the main loop
root.mainloop()
