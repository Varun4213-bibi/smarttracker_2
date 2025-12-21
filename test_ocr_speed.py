import time
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import easyocr

def test_ocr_speed(sample_texts, resolutions):
    reader = easyocr.Reader(['en'], gpu=True)
    results = []

    for text in sample_texts:
        for res in resolutions:
            # Create sample image
            img = Image.new('RGB', (800, 600), color='white')
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
            draw.text((10, 10), text, fill='black')

            # Convert to CV2
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

            # Preprocess as in optimized code
            img_cv = cv2.resize(img_cv, res)
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (3, 3), 0)
            gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

            # Time OCR
            start = time.time()
            result = reader.readtext(gray)
            end = time.time()

            ocr_time = end - start
            extracted = " ".join([res[1] for res in result])
            results.append({
                'text': text,
                'resolution': res,
                'ocr_time': ocr_time,
                'extracted': extracted
            })
            print(f"Text: {text}, Res: {res}, Time: {ocr_time:.2f}s, Extracted: {extracted}")

    return results

# Sample texts for testing
sample_texts = [
    "EXP 2025-10-19",
    "BEST BEFORE 10/2025",
    "USE BY 19-10-2025",
    "MFG SEP 2025",
    "LOT 25/09/2025"
]

# Resolutions to test (optimized is 400x300)
resolutions = [(400, 300), (800, 600)]

if __name__ == "__main__":
    print("Testing OCR speed with optimizations...")
    results = test_ocr_speed(sample_texts, resolutions)
    print("\nSummary:")
    for r in results:
        print(f"{r['text']} at {r['resolution']}: {r['ocr_time']:.2f}s")
