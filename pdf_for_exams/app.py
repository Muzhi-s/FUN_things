from pdf2image import convert_from_path
import pytesseract

def ocr_extract_text(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    
    for img in images:
        text += pytesseract.image_to_string(img, lang="chi_sim") + "\n"

    return text

pdf_path = "题1.pdf"
text = ocr_extract_text(pdf_path)
print(text)  # 你可以手动检查是否识别成功
