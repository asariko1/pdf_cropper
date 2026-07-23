#!/usr/bin/env python3
"""
PDF Crop — mark a region with your mouse, save it as a new one-page PDF.

Usage:
    python3 pdf_crop.py [optional/path/to/file.pdf]

Crop is done by copying the selected page into a new document and setting
its CropBox to the selected rectangle. This never touches the content
stream or fonts, so text stays selectable/searchable and there is no risk
of the extra-page / broken-character bugs that plague many online croppers.
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

import fitz  # PyMuPDF


ZOOM = 1.5  # rendering scale factor for on-screen preview


class PDFCropApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Crop")

        self.doc = None
        self.src_path = None
        self.page_index = 0
        self.tk_image = None  # keep a reference so Tkinter doesn't GC it

        self.rect_start = None
        self.rect_id = None
        self.selection = None  # (x0, y0, x1, y1) in canvas pixel coords

        self._build_ui()

        if len(sys.argv) > 1:
            self.load_pdf(sys.argv[1])

    def _build_ui(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        tk.Button(toolbar, text="Open PDF...", command=self.open_pdf_dialog).pack(side=tk.LEFT, padx=4, pady=4)
        tk.Button(toolbar, text="< Prev", command=self.prev_page).pack(side=tk.LEFT, padx=4)
        tk.Button(toolbar, text="Next >", command=self.next_page).pack(side=tk.LEFT, padx=4)
        self.page_label = tk.Label(toolbar, text="No file open")
        self.page_label.pack(side=tk.LEFT, padx=8)

        self.save_button = tk.Button(
            toolbar, text="Save Crop as New PDF", command=self.save_crop, state=tk.DISABLED
        )
        self.save_button.pack(side=tk.RIGHT, padx=4, pady=4)

        self.canvas = tk.Canvas(self.root, bg="gray80", cursor="cross")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

    # ---- file / page handling ----------------------------------------

    def open_pdf_dialog(self):
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if path:
            self.load_pdf(path)

    def load_pdf(self, path):
        try:
            doc = fitz.open(path)
        except Exception as exc:
            messagebox.showerror("Error", f"Could not open PDF:\n{exc}")
            return
        self.doc = doc
        self.src_path = path
        self.page_index = 0
        self.render_page()
        self.save_button.config(state=tk.NORMAL)

    def prev_page(self):
        if self.doc and self.page_index > 0:
            self.page_index -= 1
            self.render_page()

    def next_page(self):
        if self.doc and self.page_index < len(self.doc) - 1:
            self.page_index += 1
            self.render_page()

    def render_page(self):
        page = self.doc[self.page_index]
        pix = page.get_pixmap(matrix=fitz.Matrix(ZOOM, ZOOM))
        self.tk_image = tk.PhotoImage(data=pix.tobytes("ppm"))

        self.canvas.delete("all")
        self.canvas.config(width=pix.width, height=pix.height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

        self.selection = None
        self.rect_id = None
        self.page_label.config(text=f"Page {self.page_index + 1} / {len(self.doc)}  —  {os.path.basename(self.src_path)}")

    # ---- mouse selection ------------------------------------------------

    def on_mouse_down(self, event):
        if not self.doc:
            return
        self.rect_start = (event.x, event.y)
        if self.rect_id:
            self.canvas.delete(self.rect_id)
            self.rect_id = None

    def on_mouse_drag(self, event):
        if not self.rect_start:
            return
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        x0, y0 = self.rect_start
        self.rect_id = self.canvas.create_rectangle(
            x0, y0, event.x, event.y, outline="red", width=2
        )

    def on_mouse_up(self, event):
        if not self.rect_start:
            return
        x0, y0 = self.rect_start
        x1, y1 = event.x, event.y
        # normalize and clamp to canvas/image bounds
        img_w = int(self.canvas["width"])
        img_h = int(self.canvas["height"])
        x0, x1 = sorted((max(0, min(x0, img_w)), max(0, min(x1, img_w))))
        y0, y1 = sorted((max(0, min(y0, img_h)), max(0, min(y1, img_h))))
        self.rect_start = None

        if x1 - x0 < 5 or y1 - y0 < 5:
            self.selection = None
            return

        self.selection = (x0, y0, x1, y1)

    # ---- cropping / export ----------------------------------------------

    def save_crop(self):
        if not self.doc:
            return
        if not self.selection:
            messagebox.showinfo("No selection", "Drag a rectangle on the page first.")
            return

        x0, y0, x1, y1 = self.selection
        # canvas pixels -> PDF points (undo the render zoom)
        pdf_rect = fitz.Rect(x0 / ZOOM, y0 / ZOOM, x1 / ZOOM, y1 / ZOOM)

        default_name = (
            os.path.splitext(os.path.basename(self.src_path))[0]
            + f"_crop_p{self.page_index + 1}.pdf"
        )
        out_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=default_name,
            filetypes=[("PDF files", "*.pdf")],
        )
        if not out_path:
            return

        try:
            new_doc = fitz.open()
            new_doc.insert_pdf(self.doc, from_page=self.page_index, to_page=self.page_index)
            new_page = new_doc[0]
            new_page.set_cropbox(pdf_rect)
            new_doc.save(out_path)
            new_doc.close()
        except Exception as exc:
            messagebox.showerror("Error", f"Could not save crop:\n{exc}")
            return

        messagebox.showinfo("Saved", f"Cropped page saved to:\n{out_path}")


def main():
    root = tk.Tk()
    root.geometry("1000x800")
    PDFCropApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
