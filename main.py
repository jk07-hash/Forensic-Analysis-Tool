import tkinter as tk
from tkinter import filedialog, messagebox
import os
import time
import hashlib

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

report_data = ""

def calculate_hash(file_path):
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            md5.update(data)
            sha1.update(data)
            sha256.update(data)

    return md5.hexdigest(), sha1.hexdigest(), sha256.hexdigest()

def select_file():
    global report_data

    file = filedialog.askopenfilename()

    if file:
        filename = os.path.basename(file)
        filesize = os.path.getsize(file)
        created = time.ctime(os.path.getctime(file))
        modified = time.ctime(os.path.getmtime(file))

        md5_hash, sha1_hash, sha256_hash = calculate_hash(file)

        report_data = f"""
========== FORENSIC ANALYSIS REPORT ==========

File Name : {filename}

File Size : {filesize} Bytes

File Path :
{file}

Created Date :
{created}

Modified Date :
{modified}

MD5 :
{md5_hash}

SHA-1 :
{sha1_hash}

SHA-256 :
{sha256_hash}
"""

    file_text.config(state="normal")
    file_text.delete("1.0", tk.END)
    file_text.insert(tk.END, report_data)
    file_text.config(state="disabled")

def generate_report():
    global report_data

    if report_data == "":
        messagebox.showwarning("Warning", "Please Select a File First!")
        return

    with open("Forensic_Report.txt", "w") as f:
        f.write(report_data)

    messagebox.showinfo("Success", "TXT Report Saved Successfully!")

def save_pdf():
    global report_data

    if report_data == "":
        messagebox.showwarning("Warning", "Please Select a File First!")
        return

    doc = SimpleDocTemplate("Forensic_Report.pdf")
    styles = getSampleStyleSheet()

    story = []

    for line in report_data.split("\n"):
        story.append(Paragraph(line.replace(" ", "&nbsp;"), styles["BodyText"]))

    doc.build(story)

    messagebox.showinfo("Success", "PDF Report Saved Successfully!")

root = tk.Tk()
root.title("Forensic Analysis Tool")
root.geometry("900x800")

def clear_data():
    global report_data

    report_data = ""

    file_text.config(state="normal")
    file_text.delete("1.0", tk.END)
    file_text.insert("1.0", "No File Selected")
    file_text.config(state="disabled")

title = tk.Label(
    root,
    text="Forensic Analysis Tool",
    font=("Arial", 22, "bold")
)
title.pack(pady=20)

btn1 = tk.Button(root, text="Select File", width=25, font=("Arial", 12), command=select_file)
btn1.pack(pady=5)

btn2 = tk.Button(root, text="Generate TXT Report", width=25, font=("Arial", 12), command=generate_report)
btn2.pack(pady=5)

btn3 = tk.Button(root, text="Save Report as PDF", width=25, font=("Arial", 12), command=save_pdf)
btn3.pack(pady=5)

btn4 = tk.Button(
    root,
    text="Clear",
    width=25,
    font=("Arial", 12),
    command=clear_data
)
btn4.pack(pady=5)

file_text = tk.Text(root, width=100, height=20, font=("Consolas", 11))
file_text.pack(padx=20, pady=20)

file_text.insert("1.0", "No File Selected")
file_text.config(state="disabled")

root.mainloop()