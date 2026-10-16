import fitz  # PyMuPDF
import re
from typing import Dict, Any
from src.ocr import OCRExtractor

class DrawingExtractor:
    def __init__(self, pdf_path: str, tesseract_cmd: str = None):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        self.ocr_engine = OCRExtractor(tesseract_cmd=tesseract_cmd)

    def extract_data(self) -> Dict[str, Any]:
        text_blocks = []
        full_text = []

        # 1. Attempt Native Vector Text Extraction
        for page_num, page in enumerate(self.doc):
            blocks = page.get_text("blocks")
            for b in blocks:
                text_clean = b[4].strip()
                if text_clean:
                    text_blocks.append({
                        "bbox": (b[0], b[1], b[2], b[3]),
                        "text": text_clean,
                        "page": page_num
                    })
                    full_text.append(text_clean)

        combined_text = "\n".join(full_text)
        ocr_used = False

        # 2. Fallback to OCR if Native Text Extraction yields insufficient text (< 15 chars)
        if len(combined_text.strip()) < 15:
            ocr_result = self.ocr_engine.extract_from_pdf(self.pdf_path)
            combined_text = ocr_result["raw_text"]
            text_blocks = ocr_result["text_blocks"]
            ocr_used = True

        fields = self._parse_fields(combined_text)

        return {
            "raw_text": combined_text,
            "text_blocks": text_blocks,
            "fields": fields,
            "ocr_used": ocr_used
        }

    def _parse_fields(self, text: str) -> Dict[str, str]:
        dwg = re.search(r"DWG-\d{5}", text)
        rev = re.search(r"REV-[A-Z0-9]+", text)
        tol = re.search(r"ISO\s*2768-[a-zA-Z0-9]+", text, re.IGNORECASE)

        return {
            "drawing_number": dwg.group(0) if dwg else None,
            "revision": rev.group(0) if rev else None,
            "tolerance_standard": tol.group(0) if tol else None
        }