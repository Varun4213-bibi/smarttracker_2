# OCR Accuracy Improvements TODO

## Step 1: Enhance Image Preprocessing (Completed)
- [x] Update `views.py` to add Gaussian blur for noise reduction
- [x] Add adaptive thresholding for binarization
- [x] Resize images to 800x600 for consistency before OCR

## Step 2: Improve Text Correction and Normalization (Completed)
- [x] Expand correction dictionary with more entries (e.g., "EXPIRY" → "EXP", "BEST BY" → "BB")
- [x] Move corrections to a separate function for reusability
- [x] Add context-aware replacements

## Step 3: Refine Regex Patterns and Date Parsing (Completed)
- [x] Replace manual regex loops with `dateutil.parser` for robust date extraction
- [x] Add prioritization by specificity and handle ambiguities (MM/DD vs DD/MM)
- [x] Update `test_ocr.py` to reflect new logic
- [x] Add `python-dateutil` to `requirements.txt`

## Followup Steps
- [x] Install new dependencies
- [x] Run `test_ocr.py` to validate changes
- [ ] Test the app with sample images
- [ ] Monitor accuracy improvements
