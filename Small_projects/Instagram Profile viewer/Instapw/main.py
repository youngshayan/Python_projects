import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import instaloader
import requests
from io import BytesIO


def get_profile_picture(username):
    """
    Fetches the profile picture URL of the given Instagram username.

    Args:
        username (str): The Instagram username whose profile picture URL is to be fetched.

    Returns:
        str: The URL of the profile picture if found, otherwise None.
    """
    try:
        loader = instaloader.Instaloader()  # Create an instance of Instaloader
        profile = instaloader.Profile.from_username(loader.context, username)  # Get profile object
        profile_pic_url = profile.profile_pic_url  # Fetch the profile picture URL
        return profile_pic_url
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch profile picture: {e}")  # Show error message if fetching fails
        return None


def display_profile_picture():
    """
    Fetches and displays the profile picture of the entered Instagram username.
    """
    username = entry_username.get().strip()  # Get the Instagram username from the input field
    if not username:
        messagebox.showwarning("Input Error", "Please enter a username.")  # Warn the user if no username is entered
        return

    profile_pic_url = get_profile_picture(username)  # Fetch the profile picture URL
    if profile_pic_url:
        response = requests.get(profile_pic_url)  # Download the profile picture
        img_data = response.content  # Read the image data from the response
        img = Image.open(BytesIO(img_data))  # Open the image using Pillow
        img.thumbnail((300, 300))  # Resize the image to fit within the window
        img_tk = ImageTk.PhotoImage(img)  # Convert the image to a format that Tkinter can display
        label_image.config(image=img_tk)  # Update the image label to display the profile picture
        label_image.image = img_tk  # Keep a reference to the image to prevent garbage collection


# Create the main window
window = tk.Tk()  # Initialize the main application window
window.title("Instagram Profile Picture Viewer")  # Set the window title
window.geometry("400x500")  # Set the window size
window.maxsize(600, 700)
# Create GUI components
frame = tk.Frame(window)  # Create a frame to hold the input components
frame.pack(pady=20)  # Add the frame to the main window with padding

label_prompt = tk.Label(frame, text="Enter Instagram Username:")  # Create a label for the username input
label_prompt.pack(pady=5)  # Add the label to the frame

entry_username = tk.Entry(frame, width=30)  # Create an entry widget for the user to input the Instagram username
entry_username.pack(pady=5)  # Add the entry widget to the frame

button_fetch = tk.Button(frame, text="Fetch Profile Picture", command=display_profile_picture)  # Create a button to fetch the profile picture

button_fetch.pack(pady=10)  # Add the button to the frame

label_image = tk.Label(window)  # Create a label to display the profile picture
label_image.pack(pady=20)  # Add the label to the main window with padding

# Run the main loop
window.mainloop()  # Start the Tkinter event loop
