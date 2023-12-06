import os
import tkinter as tk
from PIL import Image, ImageTk
from social_media_db import initialize_db, insert_posts, get_latest_post

def resize_image(image_path, target_size=(500, 500)):
    # Open the image using Pillow
    image = Image.open(image_path)

    # Resize the image to the target size
    resized_image = image.resize(target_size)

    return resized_image

def show_image(image_path, user, text):
    root = tk.Tk()
    root.title("Social Media for Salsa cats enthusiasts")

    # Set the window size and make it non-resizable
    window_width = 500
    window_height = 900
    root.geometry(f"{window_width}x{window_height}")

    # Calculate the center coordinates of the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_center = (screen_width - window_width) // 2
    y_center = (screen_height - window_height) // 2

    # Set the window position to the center of the screen
    root.geometry(f"+{x_center}+{y_center}")

    # Set the window background color
    root.configure(bg="#accbe1")

    # Resize the image to a specific size
    resized_image = resize_image(image_path, target_size=(500, 500))

    # Create a PhotoImage object
    tk_image = ImageTk.PhotoImage(resized_image)

    # Create a frame for the Instagram-like layout
    frame = tk.Frame(root, bd=5)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Load a user icon image (replace 'path/to/user_icon.png' with the actual path)
    user_icon_path = '/Users/apatecpetschnig/Technikum_2023/SocialMediaProject/SWEG_SocialMediaProject/images/user_icon.png'
    user_icon = Image.open(user_icon_path)
    user_icon = user_icon.resize((30, 30))  # Resize the icon if needed
    tk_user_icon = ImageTk.PhotoImage(user_icon)

    # Display user icon on the top left corner
    label_user_icon = tk.Label(frame, image=tk_user_icon)
    label_user_icon.grid(row=0, column=0, sticky="w", padx=10, pady=0)

    # Display user's name next to the user icon
    label_user = tk.Label(frame, text=f"{user}", font=("Papyrus", 16, "bold"), fg="#7C98B3", anchor='w', padx=5, pady=0)
    label_user.grid(row=0, column=1, sticky="w", columnspan=2)  # Set column to 1, span 2 columns

    # Display the image with a border
    label_image = tk.Label(frame, image=tk_image, bd=2, relief="solid")
    label_image.grid(row=1, column=0, pady=10, columnspan=3)  # Span 3 columns

    # Display post text underneath the image with a border

    label_text = tk.Label(frame, text=f"{user}: {text}", font=("Courier New", 12), anchor='w', padx=10, pady=10, bd=2, relief="solid", wraplength=500)
    label_text.grid(row=2, column=0, pady=10, columnspan=3)  # Span 3 columns

    root.mainloop()


def main():
    # Initialize the database
    initialize_db()

    # Define the path to the directory containing your images
    images_directory = '/Users/apatecpetschnig/Technikum_2023/SocialMediaProject/SWEG_SocialMediaProject/posts'

    # Get a list of image files in the directory
    image_files = [f for f in os.listdir(images_directory) if f.endswith(('.jpg', '.jpeg', '.png'))]

    # Check if there are at least three image files
    if len(image_files) < 3:
        print("Error: You need at least three image files in the specified directory.")
        return

    # Use the first image files for the example posts
    posts = [
        {'image': os.path.join(images_directory, image_files[0]), 'text': 'Real Barbie after watching the Barbie movie in real life.', 'user': 'KevA'},
        {'image': os.path.join(images_directory, image_files[1]), 'text': 'Jerry has been real sad since Tom is married now.', 'user': 'Kevser'},
        {'image': os.path.join(images_directory, image_files[2]), 'text': 'Censored version of Wolf of Wall Street.', 'user': 'Kev'},
        {'image': os.path.join(images_directory, image_files[3]), 'text': 'Jack is not only drowning himself for Rose, but also choking. 😂', 'user': 'KevKev'}
    ]

    # Insert posts into the database
    insert_posts(posts)

    # Retrieve the latest post
    latest_post = get_latest_post()

    # Display the latest post
    if latest_post:
        print("Latest Post:")
        print(f"Image: {latest_post[1]}")
        print(f"Text: {latest_post[2]}")
        print(f"User: {latest_post[3]}")

        # Show the Instagram-like post in a tkinter window with additional details
        show_image(latest_post[1], latest_post[3], latest_post[2])
    else:
        print("No posts available.")

if __name__ == "__main__":
    main()
