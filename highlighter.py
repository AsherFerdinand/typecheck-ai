import fitz  # PyMuPDF
from typing import List, Dict, Any

class PDFHighlighter:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def generate_annotated_image(self, findings: List[Dict[str, Any]], page_num: int = 0, dpi: int = 150) -> bytes:
        """
        Draws colored bounding boxes on the drawing canvas:
          - Green  = Passed
          - Red    = Failed
          - Yellow = Review Required

        Renders the annotated PDF page into PNG image bytes for web display.
        """
        doc = fitz.open(self.pdf_path)
        if page_num >= len(doc):
            page_num = 0

        page = doc[page_num]

        # Define Color Palette (RGB float values 0.0 - 1.0)
        COLOR_MAP = {
            "Passed": (0.0, 0.7, 0.1),         # Green border
            "Failed": (0.9, 0.1, 0.1),         # Red border
            "Review Required": (0.95, 0.7, 0) # Yellow/Amber border
        }

        FILL_MAP = {
            "Passed": (0.8, 1.0, 0.8),         # Light Green translucent fill
            "Failed": (1.0, 0.8, 0.8),         # Light Red translucent fill
            "Review Required": (1.0, 0.95, 0.7) # Light Yellow translucent fill
        }

        for finding in findings:
            status = finding.get("status", "Review Required")
            stroke_color = COLOR_MAP.get(status, (0.5, 0.5, 0.5))
            fill_color = FILL_MAP.get(status, (0.9, 0.9, 0.9))

            # Extract target phrase from evidence string
            evidence = finding.get("evidence", "")
            target_text = None

            if "'" in evidence:
                target_text = evidence.split("'")[1]
            elif "Extracted value:" in evidence:
                target_text = evidence.replace("Extracted value:", "").strip()

            if target_text and target_text != "None":
                rects = page.search_for(target_text)
                for rect in rects:
                    # Draw translucent bounding box over detected drawing area
                    shape = page.new_shape()
                    shape.draw_rect(rect)
                    shape.finish(
                        color=stroke_color, 
                        fill=fill_color, 
                        fill_opacity=0.35, 
                        width=2
                    )
                    shape.commit()

        # Render page to high-res PNG image in memory
        pix = page.get_pixmap(dpi=dpi)
        image_bytes = pix.tobytes("png")
        doc.close()

        return image_bytes