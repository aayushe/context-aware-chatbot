import logging
import nltk
from pathlib import Path
from pdf_ocr.pdf2text import *
import contextlib
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
_here = Path(__file__).parent
nltk.download("stopwords")

with contextlib.redirect_stdout(None):
        ocr_model = ocr_predictor(
            "db_resnet50",
            "crnn_mobilenet_v3_large",
            pretrained=True,
            assume_straight_pages=True,
        )

def load_uploaded_file(file_obj, temp_dir: Path = None):
    """
    load_uploaded_file - process an uploaded file

    Args:
        file_obj (POTENTIALLY list): Gradio file object inside a list

    Returns:
        str, the uploaded file contents
    """

    # check if mysterious file object is a list
    if isinstance(file_obj, list):
        file_obj = file_obj[0]
    file_path = Path(file_obj.name)

    if temp_dir is None:
        _temp_dir = _here / "temp"
    _temp_dir.mkdir(exist_ok=True)

    try:
        pdf_bytes_obj = open(file_path, "rb").read()
        temp_path = temp_dir / file_path.name if temp_dir else file_path
        # save to PDF file
        with open(temp_path, "wb") as f:
            f.write(pdf_bytes_obj)
        logging.info(f"Saved uploaded file to {temp_path}")
        return str(temp_path.resolve())

    except Exception as e:
        logging.error(f"Trying to load file with path {file_path}, error: {e}")
        print(f"Trying to load file with path {file_path}, error: {e}")
        return None


def convert_PDF(
    pdf_obj,
    language: str = "en",
    max_pages=20,
):
    """
    convert_PDF - convert a PDF file to text

    Args:
        pdf_bytes_obj (bytes): PDF file contents
        language (str, optional): Language to use for OCR. Defaults to "en".

    Returns:
        str, the PDF file contents as text
    """
    # clear local text cache
    rm_local_text_files()
    global ocr_model
    st = time.perf_counter()
    if isinstance(pdf_obj, list):
        pdf_obj = pdf_obj[0]
    file_path = Path(pdf_obj.name)
    if not file_path.suffix == ".pdf":
        logging.error(f"File {file_path} is not a PDF file")

        html_error = f"""
        <div style="color: red; font-size: 20px; font-weight: bold;">
        File {file_path} is not a PDF file. Please upload a PDF file.
        </div>
        """
        return "File is not a PDF file", html_error, None

    conversion_stats = convert_PDF_to_Text(
        file_path,
        ocr_model=ocr_model,
        max_pages=max_pages,
    )
    converted_txt = conversion_stats["converted_text"]
    num_pages = conversion_stats["num_pages"]
    was_truncated = conversion_stats["truncated"]
    # if alt_lang: # TODO: fix this

    rt = round((time.perf_counter() - st) / 60, 2)
    print(f"Runtime: {rt} minutes")
    html = ""
    if was_truncated:
        html += f"<p>WARNING - PDF was truncated to {max_pages} pages</p>"
    html += f"<p>Runtime: {rt} minutes on CPU for {num_pages} pages</p>"
    return converted_txt, html
