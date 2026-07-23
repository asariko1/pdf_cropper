# PDF Crop

A small, self-contained tool for cropping a region out of a PDF page with your mouse and saving it as a new, single-page PDF.

Open [`pdf_crop.html`](pdf_crop.html) in any browser, drag a rectangle over the part of the page you want, and save. That's it — no installation, no account, no upload to any server.

## Why this exists

Most online "PDF crop" tools render the page, let you draw a box, and then rebuild the PDF behind the scenes. That rebuild step is where things tend to go wrong: the output gets an extra blank page, or characters come out garbled because the tool re-encoded the text and fonts incorrectly.

This tool avoids that entirely. Instead of rewriting the page's content, it copies the original page byte-for-byte and simply changes its visible boundary (the PDF `MediaBox` and `CropBox`). The text, fonts, and images are never touched, so there is nothing to corrupt and nothing that can duplicate itself into a second page.

## How to use it

1. Open `pdf_crop.html` in Chrome, Firefox, or Edge (double-click the file, or drag it into an open browser window).
2. Click **Open PDF...**, or drag and drop a PDF file onto the page.
3. All pages of the document are shown in a single scrollable view — scroll to whichever page you need.
4. Click and drag a rectangle over the region you want to keep.
5. Click **Save Crop as New PDF**. The browser downloads a new PDF containing only that one cropped page.

Only one crop is made per save. If you need several crops from the same document, repeat steps 4–5 for each one.

## What makes it safe to run anywhere

- **No installation.** It is a single HTML file. Nothing to download from an app store, no Python, no Node, no browser extension to approve.
- **No server, no upload.** Everything — opening the PDF, rendering it, and cropping it — happens locally in your browser tab. The file never leaves your computer.
- **Works offline.** All the libraries the tool needs are bundled directly inside the HTML file, so it works with no internet connection.
- **Cross-platform.** Since it's just a web page, it behaves identically on Windows and macOS, in any modern browser.

This makes it easy to distribute inside a team: email the file or drop it on a shared drive, and anyone can use it without admin rights or IT approval.

## Technical notes

- PDF rendering (so you can see and select a region) is done with [pdf.js](https://mozilla.github.io/pdf.js/).
- Building the cropped output PDF is done with [pdf-lib](https://pdf-lib.js.org/).
- The crop itself works by copying the selected page into a new one-page document and setting its `MediaBox` and `CropBox` to the selected rectangle — the same mechanism professional PDF editors use, and the reason the output keeps its original, selectable, searchable text instead of turning into a flattened image.

## Limitations

- One crop per save. The tool is intentionally simple; it does not currently support collecting several crops from different pages into a single output PDF.
- Very large PDFs (hundreds of pages) will take a few seconds longer to render, since every page is drawn when the file is opened.

## Repository contents

| File | Purpose |
|---|---|
| `pdf_crop.html` | The tool. Open this file in a browser. |
| `pdf_crop.py` | An alternative desktop version for personal use on a machine that has Python installed (Tkinter + PyMuPDF). Not needed if you're using `pdf_crop.html`. |
