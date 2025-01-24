import os
import requests
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from bs4 import BeautifulSoup
import zipfile

def download_images(query, num_images, folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = f'https://www.google.com/search?q={query}&tbm=isch'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    images = soup.find_all('img')
    count = 0
    
    for img in images[1:num_images+1]:  # Skipping the first image since it's usually Google’s logo
        img_url = img['src']
        try:
            img_data = requests.get(img_url).content
            with open(os.path.join(folder_name, f'image_{count}.jpg'), 'wb') as f:
                f.write(img_data)
            count += 1
            if count >= num_images:
                break
        except:
            continue
    
    return folder_name

def zip_folder(folder_name):
    zip_filename = f"{folder_name}.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, _, files in os.walk(folder_name):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), folder_name))
    return zip_filename

def start_scraping():
    query = entry_prompt.get()
    num_images = int(entry_num.get())
    folder_name = entry_folder.get()
    
    if not query or not num_images or not folder_name:
        messagebox.showerror("Error", "All fields are required!")
        return
    
    status_label.config(text="Downloading images...", foreground="blue")
    root.update()
    folder = download_images(query, num_images, folder_name)
    zip_file = zip_folder(folder)
    status_label.config(text=f"Success: {zip_file}", foreground="green")
    messagebox.showinfo("Success", f"Images downloaded and zipped: {zip_file}")

def browse_folder():
    folder_selected = filedialog.askdirectory()
    entry_folder.delete(0, tk.END)
    entry_folder.insert(0, folder_selected)

# Tkinter GUI setup
root = tk.Tk()
root.title("Image Scraper")
root.geometry("500x300")
root.resizable(False, False)

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

label_prompt = ttk.Label(frame, text="Enter Image Prompt:")
label_prompt.pack(anchor="w")
entry_prompt = ttk.Entry(frame, width=50)
entry_prompt.pack()

label_num = ttk.Label(frame, text="Number of Images:")
label_num.pack(anchor="w")
entry_num = ttk.Entry(frame, width=10)
entry_num.pack()

label_folder = ttk.Label(frame, text="Folder Name:")
label_folder.pack(anchor="w")
entry_folder = ttk.Entry(frame, width=50)
entry_folder.pack()
btn_browse = ttk.Button(frame, text="Browse", command=browse_folder)
btn_browse.pack()

btn_start = ttk.Button(frame, text="Start Scraping", command=start_scraping)
btn_start.pack(pady=10)

status_label = ttk.Label(frame, text="", foreground="blue")
status_label.pack()

root.mainloop()
