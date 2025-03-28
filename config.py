import os
import pytesseract
from dotenv import load_dotenv

load_dotenv()

# Configure Tesseract path
tesseract_path = os.getenv('TESSERACT_PATH')
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else:
    print("TESSERACT_PATH environment variable not set")

# Expected platforms and currencies
EXPECTED_PLATFORMS = [
    "@Yadio_io", "@CambiosRya", "@AirtmInc", 
    "@UsdtBnbVzla", "@Syklo_App", "@Mkfrontera", 
    "@BilleteraP2P", "@ElDoradoio"
]

EXPECTED_CURRENCIES = [
    "dollar", "euro", "bitcoin"
]

# Bounding boxes for image processing
BOXES_IMAGE_1 = [
    (612, 106, 865, 176), # Price box
    (50, 234, 820, 286),  # 1
    (50, 315, 820, 360),  # 2
    (50, 390, 820, 441),  # 3
    (50, 477, 820, 522),  # 4
    (50, 558, 820, 603),  # 5
    (50, 630, 820, 684),  # 6
    (50, 710, 820, 765),  # 7
    (50, 790, 820, 846)   # 8
]

BOXES_IMAGE_2 = [
    (110, 380, 450, 460),  # 1 - Dollar BCV
    (580, 370, 920, 450),  # 2 - Euro
    (588, 684, 920, 760),  # 3 - Bitcoin
]

# System prompt for AI
SYSTEM_PROMPT = '''
You are a specialized AI agent tasked with analyzing and describing images related to financial reports in Venezuela. Your response must include:
1. A detailed description of the image content
2. A strict classification according to predefined types
3. Structured JSON output

### Input Conditions:
- **image-1**: The image is a dollar report in Venezuela showing quotes from specific platforms ({EXPECTED_PLATFORMS}) published by @EnParaleloVzla3.
- **image-2**: The image displays exchange rates of the Sovereign Bolivar (Bs.) against major currencies (Euro €, Dollar $, Bitcoin ₿).

### Processing Rules:
1. **Validation**: Verify the image matches EXACTLY one of the conditions above
2. **Type Handling**: 
   - If multiple conditions apply, prioritize image-1 over image-2
   - If no conditions match, return type 'null'.

### Output Format:
- **value**: The type of the image ('image-1', 'image-2', 'null')
'''.format(EXPECTED_PLATFORMS=', '.join(EXPECTED_PLATFORMS))