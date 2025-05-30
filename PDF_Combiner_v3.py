import os
import fitz   # pip install PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox

def combine_pdfs():
    # hide the root TK window
    root = tk.Tk(); root.withdraw()

    # select input PDFs
    pdf_files = filedialog.askopenfilenames(
        title="Select PDF files to combine",
        filetypes=[("PDF files", "*.pdf")])
    if not pdf_files:
        return

    # ask where to save the merged PDF (and what name)
    output_path = filedialog.asksaveasfilename(
        title="Save combined PDF as…",
        defaultextension=".pdf",
        initialfile="combined.pdf",
        filetypes=[("PDF files", "*.pdf")])
    if not output_path:
        return

    # open a new (empty) document
    out_doc = fitz.open()

    for src_path in pdf_files:
        src = fitz.open(src_path)
        for pno in range(src.page_count):
            page = src[pno]
            text = page.get_text("text").strip()
            annots = page.annots()
            # consider it “non-blank” if there’s text, images, or any annotation
            if text or list(annots or []):
                out_doc.insert_pdf(src, from_page=pno, to_page=pno)
            else:
                print(f"Skipping blank page {pno+1} of {os.path.basename(src_path)}")

    try:
        out_doc.save(output_path)
     
    except Exception as e:
        messagebox.showerror("Error saving", str(e))
    finally:
        out_doc.close()
        root.destroy()

if __name__ == "__main__":
    combine_pdfs()
