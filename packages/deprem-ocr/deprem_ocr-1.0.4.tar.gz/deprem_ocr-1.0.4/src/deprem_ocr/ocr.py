import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import time
import tarfile
import requests
from io import BytesIO

from src.deprem_ocr import utility
from src.deprem_ocr.detector import TextDetector
from src.deprem_ocr.recognizer import TextRecognizer

__all__ = ["DepremOCR"]

class DepremOCR:
    def __init__(self):
        self.__download_models()

        args = utility.parse_args()
        self.text_recognizer = TextRecognizer(args)
        self.text_detector = TextDetector(args)

    def apply_ocr(self, img):
        # Detect text regions
        dt_boxes, _ = self.text_detector(img)

        boxes = []
        for box in dt_boxes:
            p1, p2, p3, p4 = box
            x1 = min(p1[0], p2[0], p3[0], p4[0])
            y1 = min(p1[1], p2[1], p3[1], p4[1])
            x2 = max(p1[0], p2[0], p3[0], p4[0])
            y2 = max(p1[1], p2[1], p3[1], p4[1])
            boxes.append([x1, y1, x2, y2])

        # Recognize text
        img_list = []
        for i in range(len(boxes)):
            x1, y1, x2, y2 = map(int, boxes[i])
            img_list.append(img.copy()[y1:y2, x1:x2])
        img_list.reverse()

        rec_res, _ = self.text_recognizer(img_list)

        # Postprocess
        total_text = ""
        for i in range(len(rec_res)):
            total_text += rec_res[i][0] + " "

        total_text = total_text.strip()
        return total_text

    def __download_models(self):
        det_model_path = "ch_PP-OCRv3_det_infer"
        if not os.path.exists(det_model_path):
            det_model_url = "https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_det_infer.tar"
            self.__download_file(det_model_path, det_model_url)
            self.__extract_tar(det_model_path)

        rec_model_path = "ch_PP-OCRv3_rec_infer"
        if not os.path.exists(rec_model_path):
            rec_model_url = "https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_rec_infer.tar"
            self.__download_file(rec_model_path, rec_model_url)
            self.__extract_tar(rec_model_path)

    def __download_file(self, path: str, url: str):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(path, 'wb') as f:
                f.write(response.raw.read())

    def __extract_tar(self, path: str):
        model_tar = tarfile.open(path+".tar")
        model_tar.extractall('./')
        model_tar.close()
        
def main():
    import numpy as np
    from PIL import Image

    image_url = "https://i.ibb.co/kQvHGjj/aewrg.png"
    response = requests.get(image_url)
    img = np.array(Image.open(BytesIO(response.content)).convert("RGB"))

    depremOCR = DepremOCR()

    t0 = time.time()
    epoch = 1
    for _ in range(epoch):
        ocr_text = depremOCR.apply_ocr(img)
    print("Elapsed time:", (time.time() - t0) * 1000 / epoch, "ms")

    print("Output:", ocr_text)


if __name__ == "__main__":
    main()
