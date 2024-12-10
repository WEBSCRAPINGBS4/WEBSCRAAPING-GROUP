import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
from io import BytesIO
from urllib.parse import urljoin

# Function to scrape the webpage
def scrape_website():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a URL to scrape.")
        return

    try:
        # Fetch the webpage
        response = requests.get(url)
        response.raise_for_status()  # Raise error if the request failed

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        
        # Get title
        title = soup.title.string if soup.title else "No title found"

        # Get text content
        paragraphs = soup.find_all('p')
        text_content = "\n\n".join([p.get_text() for p in paragraphs[:5]])  # First 5 paragraphs

        # Display title and text content
        title_label.config(text="Title: " + title)
        text_display.config(state=tk.NORMAL)
        text_display.delete(1.0, tk.END)
        text_display.insert(tk.END, text_content)
        text_display.config(state=tk.DISABLED)
        
        # Display images (limit to first 5 images)
        images = soup.find_all('img')
        for widget in image_frame.winfo_children():
            widget.destroy()  # Clear previous images

        for img_tag in images[:5]:
            img_url = img_tag.get("src")
            img_url = urljoin(url, img_url)  # Make sure it's an absolute URL
            
            # Fetch and display the image
            img_response = requests.get(img_url)
            img_data = Image.open(BytesIO(img_response.content))
            img_data.thumbnail((100, 100))  # Resize for display
            img = ImageTk.PhotoImage(img_data)
            img_label = tk.Label(image_frame, image=img)
            img_label.image = img  # Keep a reference to avoid garbage collection
            img_label.pack(side=tk.LEFT, padx=5, pady=5)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to retrieve data: {e}")

# GUI setup
root = tk.Tk()
root.title("Web Scraping App")
root.geometry("600x600")
root.config(bg="lightblue")

# Title Label
header_label = tk.Label(root, text="Web Scraping App", font=("Arial", 18, "bold"), bg="lightblue", fg="darkblue")
header_label.pack(pady=10)

# URL Entry
url_label = tk.Label(root, text="Enter URL:", font=("Arial", 12), bg="lightblue")
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Scrape Button
scrape_button = tk.Button(root, text="Scrape", font=("Arial", 12, "bold"), bg="green", fg="white", command=scrape_website)
scrape_button.pack(pady=10)

# Title Display
title_label = tk.Label(root, text="Title:", font=("Arial", 12), bg="lightblue")
title_label.pack(pady=10)

# Text Display
text_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10, font=("Arial", 10))
text_display.config(state=tk.DISABLED)
text_display.pack(pady=10)

# Image Display
image_frame = tk.Frame(root, bg="lightblue")
image_frame.pack(pady=10)

# Run the Tkinter main loop
root.mainloop()
