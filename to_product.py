import os
import string
from PIL import Image, ImageDraw, ImageFont  # 画像関連を扱うのに便利なPILモジュールをインポート
from modules.analyze_cross_map import make_words_list

WHITE_CELL_COLOR = (255, 255, 255)
ANSWER_CELL_COLOR = (200, 200, 200)


def cross_map_to_img(
    cross_map,
    H,
    W,
    question_index_list,
    answer_index_list=[],
    q_save_path=".\\q.png",
    a_save_path=".\\a.png",
):
    """
    cross_mapを元に画像を生成する
    cross_mapは2次元配列を想定
    params:
        cross_map:2次元のクロスワードの盤面
        H:高さ
        W:幅
        question_index_list:問題のインデックスのリスト (x:int,y:int,index:str)
        answer_index_list:解答のインデックスリスト (x:int,y:int,index:str)
        v_word_description:縦の単語の説明文
        h_word_description:横の単語の説明文
        q_save_path:問題盤面画像の保存パス
        a_save_path:解答盤面画像の保存パス
    """
    im = Image.new(
        "RGB", (50 * H + 1, 50 * W + 1), (0, 0, 0)
    )  # 下地となる画像生成、マスのかずだけサイズの大きな画像になるように設定
    im2 = Image.new(
        "RGB", (50 * H + 1, 50 * W + 1), (0, 0, 0)
    )  # 二つ目を作るのは問題用と回答用の画像２枚を出力するため
    draw = ImageDraw.Draw(im)  # 問題側の盤面
    draw2 = ImageDraw.Draw(im2)  # 解答側の盤面

    # 問題インデックスの配置マップ作成
    question_index_map = [[None] * W for s in range(H)]
    for i in question_index_list:
        question_index_map[i[1]][i[0]] = i[2]

    # 答えのインデックスの配置マップの作成
    answer_index_map = [[None] * W for s in range(H)]
    for i in answer_index_list:
        answer_index_map[i[1]][i[0]] = i[2]

    def write_cell(x, y, string, question_index, answer_index):
        font_main = ImageFont.truetype("meiryo.ttc", 35)  # メイン文字のフォントとサイズ
        font_index = ImageFont.truetype("meiryo.ttc", 15)  # インデックス文字のフォントとサイズ

        # 問題側のマスを作成
        if string != "黒":  # 黒マスじゃない場合
            # 背景色の決定
            if answer_index:
                draw.rectangle(
                    (1 + (x) * 50, 1 + (y) * 50, 49 + (x) * 50, 49 + (y) * 50),
                    fill=ANSWER_CELL_COLOR,
                    outline=ANSWER_CELL_COLOR,
                )  # 解答キーマスの灰色を書き込み
            else:
                draw.rectangle(
                    (1 + (x) * 50, 1 + (y) * 50, 49 + (x) * 50, 49 + (y) * 50),
                    fill=WHITE_CELL_COLOR,
                    outline=WHITE_CELL_COLOR,
                )  # 通常白マスを書き込み

            # 問題のインデックスの書き込み
            if question_index:
                print(
                    "q_write x:{} y:{} w:{}".format(
                        1 + (x) * 50, 1 + y * 50, question_index
                    )
                )
                draw.text(
                    (1 + (x) * 50, 1 + (y) * 50),
                    question_index,
                    fill=(0, 0, 0),
                    font=font_index,
                )

            # 答えのインデックスの書き込み
            if answer_index:
                print(
                    "a_write x:{} y:{} w:{}".format(
                        49 + x * 50, -1 + y * 50, answer_index
                    )
                )
                draw.text(
                    (49 + x * 50, 49 + y * 50),
                    answer_index,
                    anchor="rb",
                    fill=(0, 0, 0),
                    font=font_index,
                )  # 数字書き込み

        else:  # 黒マスの場合
            if question_index or answer_index:
                raise Exception(
                    "パラメータの指定に矛盾が生じています。x:{} y:{} string:{} question_index:{} answer_index:{}".format(
                        x, y, string, question_index, answer_index
                    )
                )

        # 解答側のマスを作成
        if string != "黒":  # 黒マスじゃない場合
            # 背景色の決定
            if answer_index:
                draw2.rectangle(
                    (1 + (x) * 50, 1 + (y) * 50, 49 + (x) * 50, 49 + (y) * 50),
                    fill=ANSWER_CELL_COLOR,
                    outline=ANSWER_CELL_COLOR,
                )  # 少しサイズの小さい白い四角形の画像を上書き
            else:
                draw2.rectangle(
                    (1 + (x) * 50, 1 + (y) * 50, 49 + (x) * 50, 49 + (y) * 50),
                    fill=WHITE_CELL_COLOR,
                    outline=WHITE_CELL_COLOR,
                )  # 少しサイズの小さい白い四角形の画像を上書き
            draw2.text(
                (7.5 + (x) * 50, (y) * 50), string, fill=(0, 0, 0), font=font_main
            )  # 文字の書き込み
        else:  # 黒マスだったら何もしない
            pass

    for i in range(W):
        for j in range(H):
            write_cell(
                i, j, cross_map[j][i], question_index_map[j][i], answer_index_map[j][i]
            )

    im.save(a_save_path, quality=95)  # 完成した画像を出力
    im2.save(q_save_path, quality=95)  # 完成した画像を出力


def words_to_png(v_words, h_words, dict, description_save_path):
    font_size = 15
    font_description = ImageFont.truetype("meiryo.ttc", font_size)  # メイン文字のフォントとサイズ
    line_height = 20
    img_height = line_height * (len(v_words) + len(h_words) + 3)
    img_width = 200

    description_number_width = font_size * 2

    im = Image.new(
        "RGB", (img_width, img_height), (255, 255, 255)
    )  # 下地となる画像生成、マスのかずだけサイズの大きな画像になるように設定
    draw = ImageDraw.Draw(im)  # 問題側の盤面

    line_count = 0
    draw.text(
        (1, line_count * line_height), "縦の鍵", fill=(0, 0, 0), font=font_description
    )

    for i in v_words:
        line_count += 1
        num_string = str(i[3]) + "."
        draw.text(
            (-1 + description_number_width, line_count * line_height),
            num_string,
            fill=(0, 0, 0),
            anchor="ra",
            font=font_description,
        )
        draw.text(
            (1 + description_number_width, line_count * line_height),
            dict.get(i[2], ""),
            fill=(0, 0, 0),
            font=font_description,
        )
    line_count += 2
    draw.text(
        (1, line_count * line_height), "横の鍵", fill=(0, 0, 0), font=font_description
    )
    for i in h_words:
        line_count += 1
        num_string = str(i[3]) + "."
        draw.text(
            (-1 + description_number_width, line_count * line_height),
            num_string,
            fill=(0, 0, 0),
            anchor="ra",
            font=font_description,
        )
        draw.text(
            (1 + description_number_width, line_count * line_height),
            dict.get(i[2], ""),
            fill=(0, 0, 0),
            font=font_description,
        )

    im.save(description_save_path, quality=95)


def to_product(
    cross_map,
    answer_index_list=None,
    question_img_file_name: str = "question.png",
    answer_img_file_name: str = "answer.png",
    v_words_file_name: str = None,
    h_words_file_name: str = None,
    description_dict: dict = {},
    description_img_file_name: str = "description.png",
):
    """
    プロダクトを作成する
    params:
        cross_map:盤面情報(2次元配列)
        answer_index_list:答えのインデックスのリスト
        question_img_file_name:問題画像のファイル名
        answer_img_file_name:解答画像のファイル名
        v_words_file_name:縦方向の単語一覧
        h_words_file_name:横方向の単語一覧
    """

    v_words, h_words = make_words_list(cross_map, len(cross_map), len(cross_map[0]))
    print(v_words, h_words)

    words_to_png(v_words, h_words, description_dict, description_img_file_name)
    question_index_list = [(s[0], s[1], str(s[3])) for s in v_words + h_words]
    cross_map_to_img(
        cross_map,
        H,
        W,
        question_index_list,
        answer_index_list,
        question_img_file_name,
        answer_img_file_name,
    )

    # 縦方向の単語一覧をファイルに保存
    v_strings = ""
    for i in v_words:
        v_strings += "{},{}\n".format(i[3], i[2])
    with open(v_words_file_name, "w", encoding="utf-8") as f:
        f.write(v_strings)

    # 横方向の単語一覧をファイルに保存
    h_strings = ""
    for i in h_words:
        h_strings += "{},{}\n".format(i[3], i[2])
    with open(h_words_file_name, "w", encoding="utf-8") as f:
        f.write(h_strings)


def parse_search(f_path, answer_index_character_map: str = string.ascii_uppercase):
    """
    search_crossから出力されたファイルを読み取る
    """
    with open(f_path, "r", encoding="utf-8") as f:
        H, W = f.readline().strip().split(",")
        H = int(H)
        W = int(W)
        cross_map = []
        for _ in range(H):
            h_line = f.readline().strip().split(",")
            if len(h_line) != W:
                raise Exception(
                    "縦横サイズと盤面のサイズが違います H:{} W:{} h_line:{}".format(H, W, h_line)
                )
            cross_map.append(h_line)
        answer_index_list = []
        answer_temps = f.readlines()
        for idx, i in enumerate(answer_temps):
            i = i.strip().split(",")
            answer_index_list.append(
                (int(i[0]), int(i[1]), answer_index_character_map[idx])
            )
        return H, W, cross_map, answer_index_list


if __name__ == "__main__":
    import os
    import json

    # 入力指定
    path = os.path.join("test_data", "to_product_test.txt")  # search_cross.pyの出力ファイルを指定
    description_path = os.path.join("test_data", "test_dic.json")  # 単語の説明ファイルを指定

    # 成果物のファイル名指定
    product_name = "test"  # 成果物を保存するフォルダ名
    q_png_name = "img_q_test.png"  # 問題用画像生成ファイル名
    a_png_name = "img_a_test.png"  # 解答用画像生成ファイル名
    v_word_name = "key_v.txt"  # 縦の鍵一覧番号生成ファイル名
    h_word_name = "key_h.txt"  # 横の鍵一覧番号生成ファイル名
    description_name = "description.png"  # ヒント文生成画像ファイル名

    H, W, cross_map, answer_index_list = parse_search(path)

    save_dir = os.path.join("product", product_name)
    os.makedirs(save_dir, exist_ok=True)

    with open(description_path, "r", encoding="utf-8") as f:
        description_dic = json.load(f)

    q_save_path = os.path.join(save_dir, q_png_name)
    a_save_path = os.path.join(save_dir, a_png_name)
    v_word_save_path = os.path.join(save_dir, v_word_name)
    h_word_save_path = os.path.join(save_dir, h_word_name)
    description_save_path = os.path.join(save_dir, description_name)
    to_product(
        cross_map,
        answer_index_list,
        q_save_path,
        a_save_path,
        v_word_save_path,
        h_word_save_path,
        description_dic,
        description_save_path,
    )
