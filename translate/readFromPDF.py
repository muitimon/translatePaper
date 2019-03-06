#以下のページを参照
#https://qiita.com/mczkzk/items/894110558fb890c930b5
import sys

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTContainer, LTTextBox
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage


def find_textboxes_recursively(layout_obj):
    """
    再帰的にテキストボックス（LTTextBox）を探して、テキストボックスのリストを取得する。
    """
    # LTTextBoxを継承するオブジェクトの場合は1要素のリストを返す。
    if isinstance(layout_obj, LTTextBox):
        return [layout_obj]

    # LTContainerを継承するオブジェクトは子要素を含むので、再帰的に探す。
    if isinstance(layout_obj, LTContainer):
        boxes = []
        for child in layout_obj:
            boxes.extend(find_textboxes_recursively(child))

        return boxes

    return []  # その他の場合は空リストを返す。

# Layout Analysisのパラメーターを設定。縦書きの検出を有効にする。
laparams = LAParams(detect_vertical=True)

# 共有のリソースを管理するリソースマネージャーを作成。
resource_manager = PDFResourceManager()

# ページを集めるPageAggregatorオブジェクトを作成。
device = PDFPageAggregator(resource_manager, laparams=laparams)

# Interpreterオブジェクトを作成。
interpreter = PDFPageInterpreter(resource_manager, device)

# 出力用のテキストファイル
output_txt = open('output.txt', 'w')

def sortForPaper(boxes_obj, page_obj):
    """
    ページの左右にリストを分けてsortを行う
    """
    boxes_right = []
    boxes_left = []

    # ページの右半分，左半分の要素に分ける
    for box_obj in boxes_obj:
        if box_obj.x0 > page_obj.mediabox[2]/2:
            boxes_right.append(box_obj)
        else:
            boxes_left.append(box_obj)

    # 高さ順に並べ替え
    boxes_right.sort(key=lambda b: -b.y1)
    boxes_left.sort(key=lambda b: -b.y1)
    boxes_left.extend(boxes_right)

    return boxes_left

with open(sys.argv[1], 'rb') as f:
    # PDFPage.get_pages()にファイルオブジェクトを指定して、PDFPageオブジェクトを順に取得する。
    # 時間がかかるファイルは、キーワード引数pagenosで処理するページ番号（0始まり）のリストを指定するとよい。
    for page in PDFPage.get_pages(f):
        interpreter.process_page(page)  # ページを処理する。
        layout = device.get_result()  # LTPageオブジェクトを取得。

        # ページ内のテキストボックスのリストを取得する。
        boxes = find_textboxes_recursively(layout)

        # ページを記述順にならべかえる
        boxes_paper = sortForPaper(boxes, page)

        for box in boxes_paper:
            print(box.get_text().strip())  # テキストボックス内のテキストを表示する。
