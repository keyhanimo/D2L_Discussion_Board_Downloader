import tkinter as tk
from tkinter import filedialog, simpledialog, scrolledtext
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from pathlib import Path
import threading
import os
import time

# Function to create the initial GUI
def create_initial_gui():
    global text_box
    # Create the main window
    root = tk.Tk()
    root.title("D2L Discussion Board Downloader")

    # Set window size and position
    window_width = 600
    window_height = 800
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    # Add a frame to contain the welcome message and button
    frame = tk.Frame(root, bg='#f0f0f0', bd=10)
    frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

    # Add a welcome message
    welcome_message = "Welcome to the D2L Discussion Board Downloader!\n\n" \
                      "This tool helps you download all attachment files from a D2L discussion board and save them to your computer such that each file name begins with the last name of the submitter.\n" \
                      "Requirements: Windows OS, Chrome browser.\n\n" \
                      "Before you start, please ensure you have:\n" \
                      "- The latest version of Chrome browser installed.\n" \
                      "- The latest version of chromedriver installed from: https://chromedriver.chromium.org/downloads\n" \
                      "- The URL of the D2L discussion board's first page (ends with 'View').\n\n" \
                      "Click START to begin.\n\n" \
                      "After inputs are provided, the tool will ask you to log in to D2L. This tool is completely private, fully runs on your local computer and does not store or send information anywhere else.\n\n" \
                      "Version 1.0 by Dr. Mohammad Keyhani (www.digitvibe.com), made on April 3, 2024 with ChatGPT"
    label = tk.Label(frame, text=welcome_message, justify=tk.CENTER, bg='#f0f0f0', wraplength=500)
    label.pack(pady=10)

    # Add a START button
    start_button = tk.Button(frame, text='START', command=lambda: start_download(root), height=2, width=10, bg='#4CAF50', fg='white', font=('Helvetica', 12, 'bold'))
    start_button.pack(pady=10)

    # Add a text box for progress updates
    text_box = scrolledtext.ScrolledText(frame, width=60, height=100, state='disabled')
    text_box.pack(pady=10)

    return root

# Function to start the download process
def start_download(root):
    global stop_requested
    stop_requested = False

    # Disable the START button and change it to a STOP button
    start_button = root.nametowidget('.!frame.!button')
    start_button.config(text='STOP', command=lambda: stop_download(root), bg='#f44336')

    # Enable the text box for progress updates
    text_box.config(state='normal')
    text_box.delete(1.0, tk.END)

    base_url = simpledialog.askstring("Input", "Enter the D2L discussion board URL:", parent=root)
    if base_url is None:  # User clicked Cancel
        reset_gui(root)
        return

    download_dir = filedialog.askdirectory(title="Select download directory", parent=root)
    if not download_dir:  # User clicked Cancel
        reset_gui(root)
        return
    download_dir = Path(download_dir)

    # Start the download process in a separate thread
    threading.Thread(target=download_process, args=(root, base_url, download_dir)).start()

# Function to stop the download process
def stop_download(root):
    global stop_requested
    stop_requested = True

    # Print a message in the text box
    text_box.insert(tk.END, "Stopping...\n")
    text_box.see(tk.END)

# Function to handle the download process
def download_process(root, base_url, download_dir):
    # Set up Chrome options for the webdriver
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_experimental_option('prefs', {
        "download.default_directory": str(download_dir),  # Set the download directory
        "download.prompt_for_download": False,  # Disable download prompts
        "download.directory_upgrade": True,  # Enable directory upgrade
        "safebrowsing.enabled": True,  # Enable safe browsing
        "plugins.always_open_pdf_externally": True  # Open PDFs externally
    })

    # Initialize the Chrome webdriver with the options
    driver = webdriver.Chrome(options=options)
    # Set up a wait object to wait for elements to load
    wait = WebDriverWait(driver, 10)

    # Start processing pages
    page_number = 1
    while not stop_requested:  # Continue until stop is requested
        # Construct the URL for the current page
        d2l_url = f"{base_url}?pageNumber={page_number}&groupFilterOption=0"
        # Open the page in the browser
        driver.get(d2l_url)

        # Update the text box with the current page being processed
        update_text_box(f"Processing page {page_number}...\n")

        try:
            # Wait for the page to load by waiting for an element to be present
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'd2l-filelink-text')))
        except TimeoutException:  # If the page takes too long to load or has no content
            update_text_box(f"No more content on page {page_number}. Exiting.\n")
            break  # Exit the loop

        # Find all posts with attachments
        posts_with_attachments = driver.find_elements(By.XPATH, '//li[contains(@class, "d2l-datalist-item") and .//a[contains(@class, "d2l-filelink-text")]]')
        # Update the text box with the number of posts with attachments
        update_text_box(f"Number of posts with attachments: {len(posts_with_attachments)}\n")

        # If there are no posts with attachments, exit the loop
        if len(posts_with_attachments) == 0:
            update_text_box("No more posts with attachments. Exiting.\n")
            break

        # Iterate through each post with attachments
        for post in posts_with_attachments:
            if stop_requested:  # If stop is requested, break the loop
                break

            # Find the student's full name from the post
            student_info_element = post.find_element(By.XPATH, './/div[contains(@class, "d2l-textblock-secondary")]')
            student_info_text = student_info_element.text
            student_full_name = student_info_text.split('posted')[0].strip()

            # Find all attachment elements in the post
            attachment_elements = post.find_elements(By.CLASS_NAME, 'd2l-filelink-text')

            # Iterate through each attachment
            for attachment in attachment_elements:
                if stop_requested:  # If stop is requested, break the loop
                    break

                # Extract the original file name from the attachment
                original_filename = attachment.text
                # Split the full name into parts and format the new file name
                name_parts = student_full_name.split()
                last_name = name_parts[-1] if name_parts else "~"
                new_filename = f"{last_name}_{student_full_name.replace(' ', '_')}_{original_filename}"

                # Scroll the attachment into view and then click it to initiate download
                driver.execute_script("arguments[0].scrollIntoView();", attachment)
                driver.execute_script("arguments[0].click();", attachment)

                # Wait for the new file to appear in the download directory
                initial_files = os.listdir(download_dir)
                while not stop_requested:
                    time.sleep(1)
                    current_files = os.listdir(download_dir)
                    new_files = [f for f in current_files if f not in initial_files]
                    if new_files:
                        downloaded_file = max(new_files, key=lambda f: os.path.getctime(download_dir / f))
                        if not downloaded_file.endswith('.crdownload'):
                            break  # Break the loop once the download is complete

                # If stop is not requested, rename the downloaded file
                if not stop_requested:
                    downloaded_file = max(new_files, key=lambda f: os.path.getctime(download_dir / f))
                    original_file_path = download_dir / downloaded_file
                    new_file_path = download_dir / new_filename
                    os.replace(original_file_path, new_file_path)  # Replace the original file with the new file

                    # Update the text box with the downloaded file information
                    update_text_box(f"File downloaded and renamed to: {new_file_path}\n")

        # Increment the page number for the next iteration
        page_number += 1

    # Quit the webdriver and reset the GUI once the process is complete or stopped
    driver.quit()
    reset_gui(root)


# Function to reset the GUI after the download process is complete or stopped
def reset_gui(root):
    if stop_requested:
        update_text_box("Download stopped by user.\n")
    else:
        update_text_box("Download completed.\n")

    # Re-enable the START button
    start_button = root.nametowidget('.!frame.!button')
    start_button.config(text='START', command=lambda: start_download(root), bg='#4CAF50')

    # Disable the text box
    text_box.config(state='disabled')

# Function to update the text box with progress messages
def update_text_box(message):
    text_box.insert(tk.END, message)
    text_box.see(tk.END)
    text_box.update()

# Main function to start the application
def main():
    root = create_initial_gui()
    root.mainloop()

if __name__ == "__main__":
    main()
