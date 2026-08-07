# PDF Crop

A small, self-contained tool for cropping a region out of a PDF page with your mouse and saving it as a new, single-page PDF.

**Use it here: [pdfcrop.asariko.net](https://pdfcrop.asariko.net)**

Or download [`index.html`](index.html) and open it in any browser — it works exactly the same offline. Drag a rectangle over the part of the page you want, and save. That's it — no installation, no account, no upload to any server.

## Why this exists

Most online "PDF crop" tools render the page, let you draw a box, and then rebuild the PDF behind the scenes. That rebuild step is where things tend to go wrong: the output gets an extra blank page, or characters come out garbled because the tool re-encoded the text and fonts incorrectly.

This tool avoids that entirely. Instead of rewriting the page's content, it copies the original page byte-for-byte and simply changes its visible boundary (the PDF `MediaBox` and `CropBox`). The text, fonts, and images are never touched, so there is nothing to corrupt and nothing that can duplicate itself into a second page.

## How to use it

1. Open [pdfcrop.asariko.net](https://pdfcrop.asariko.net), or double-click your downloaded copy of `index.html`.
2. Click **Open PDF...**, or drag and drop a PDF file onto the page.
3. All pages of the document are shown in a single scrollable view — scroll to whichever page you need.
4. Click and drag a rectangle over the region you want to keep.
5. Click **Save Crop as New PDF**. The browser downloads a new PDF containing only that one cropped page.

Only one crop is made per save. If you need several crops from the same document, repeat steps 4–5 for each one.

## What makes it safe to run anywhere

- **No installation.** It is a single HTML file. Nothing to download from an app store, no Python, no Node, no browser extension to approve.
- **No server, no upload.** Everything — opening the PDF, rendering it, and cropping it — happens locally in your browser tab. The file never leaves your computer.
- **Works offline.** Every library the tool needs is bundled directly inside `index.html`, so a downloaded copy works with no internet connection.
- **Cross-platform.** Since it's just a web page, it behaves identically on Windows and macOS, in any modern browser.

This makes it easy to distribute inside a team: send the file or drop it on a shared drive, and anyone can use it without admin rights or IT approval.

## Technical notes

- PDF rendering (so you can see and select a region) is done with [pdf.js](https://mozilla.github.io/pdf.js/).
- Building the cropped output PDF is done with [pdf-lib](https://pdf-lib.js.org/).
- Both libraries are inlined into `index.html`, which is why the file is large (~2.3 MB) and why it needs no network access.
- The crop itself works by copying the selected page into a new one-page document and setting its `MediaBox` and `CropBox` to the selected rectangle — the same mechanism professional PDF editors use, and the reason the output keeps its original, selectable, searchable text instead of turning into a flattened image.

## Limitations

- One crop per save. The tool is intentionally simple; it does not currently support collecting several crops from different pages into a single output PDF.
- Very large PDFs (hundreds of pages) will take a few seconds longer to render, since every page is drawn when the file is opened.

## Repository contents

| File | Purpose |
|---|---|
| `index.html` | The tool. Open this file in a browser, or visit the hosted version. |
| `pdf_crop.py` | An alternative desktop version for personal use on a machine that has Python installed (Tkinter + PyMuPDF). Not needed if you're using `index.html`. |
| `assets/`, `style.css`, `script.js`, `tailwind.css` | Site styling and shared header/footer behaviour for the hosted page. |
| `tailwind.config.js`, `in.css` | Build inputs used to regenerate `tailwind.css`. Not needed at runtime. |
| `CNAME` | Custom domain for GitHub Pages. |

To regenerate the stylesheet after changing any classes in `index.html`:

```bash
npx tailwindcss@3 -c tailwind.config.js -i in.css -o tailwind.css --minify
```

## License

Free to use, not for sale. Licensed under the [PolyForm Noncommercial License 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0) — see [LICENSE](LICENSE).

You may use, copy, modify and share it for personal, research, educational, charitable and government purposes. You may not sell it or use it commercially.
