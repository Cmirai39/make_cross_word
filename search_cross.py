import os
import itertools
from tqdm import tqdm

VERTICAL = 1
HORIZONTAL = 2


def right_word(x, y, cross_map, W):
    """
    右側に言葉があるかどうかを確認する
    あれば、その言葉を返す
    params:
        x:スタートのx座標
        y:スタートのy座標
        cross_map:クロスワードの盤面の2次元配列
        W:クロスワードの盤面の幅
    """

    if x >= 1 and cross_map[y][x - 1] != "黒":
        return ""

    i = 0
    ret = ""
    while True:
        if x + i < W:
            if cross_map[y][x + i] == "黒":
                break
            else:
                ret += cross_map[y][x + i]
            i += 1
        else:
            break

    if i == 0 or i == 1:
        return ""
    else:
        return ret


def down_word(x, y, cross_map, H):
    """
    下側に言葉があるかどうかを確認する
    あれば、その言葉を返す
    params:
        x:スタートのx座標
        y:スタートのy座標
        cross_map:クロスワードの盤面の2次元配列
        H:クロスワードの盤面の高さ
    """
    if y >= 1 and cross_map[y - 1][x] != "黒":
        return ""
    i = 0
    ret = ""
    while True:
        if y + i < H:
            if cross_map[y + i][x] == "黒":
                break
            else:
                ret += cross_map[y + i][x]
            i += 1
        else:
            break
    if i == 0 or i == 1:
        return ""
    else:
        return ret


class Word:
    """
    キー文字が何個含まれているか、また隣接する単語を保存するクラス
    """

    def __init__(self, x, y, length, orient):
        self.next = []
        self.is_key = 0

        self.coords = []
        if orient == VERTICAL:
            for i in range(length):
                self.coords.append((x, y + i))
        elif orient == HORIZONTAL:
            for i in range(length):
                self.coords.append((x + i, y))
        else:
            raise Exception("予期しない orient:{}".format(orient))

    def add_next(self, idx):
        self.next.append(idx)

    def get_next(self):
        return self.next

    def get_is_key(self):
        return self.is_key

    def check_is_key(self, key_coords):
        """
        自分が含んでいるキー文字数を返す
        params:
            key_coords:キーの座標のリスト(0,0),(2,3)など
        """
        self.is_key = 0
        for i in self.coords:
            if i in key_coords:
                self.is_key += 1
        return self.is_key

    def __str__(self):
        string = "\n"
        string += "座標一覧:{}\n".format(",".join([str(s) for s in self.coords]))
        string += "キー文字の数:{}\n".format(self.is_key)
        string += "隣の文字一覧:{}\n".format(self.next)
        return string


def validate(word, cross):
    """
    クロスワードの盤面評価を行う。
    分散具合が大きいほど大きな評価になる。
    params:
        word:最終的な言葉
        cross:2次元の配列
    """
    # キーに含まれる文字がそれぞれいくつあるかカウント
    word_dic = {}
    for i in word:
        word_dic[i] = word_dic.get(i, 0) + 1

    coord_dic = {}  # キーに使われている文字の座標を保存する辞書
    # 初期化
    for i in word_dic.keys():
        coord_dic[i] = []
    # それぞれの文字の座標をリストとして保存
    for j in range(H):
        for i in range(W):
            if cross[j][i] in coord_dic.keys():
                coord_dic[cross[j][i]].append((i, j))

    # word_liの該当するWordインスタンスにアクセスするためのインデックス(step)を保存する配列の初期化
    h_step_map = [[-1 for i in range(len(cross[0]))] for j in range(len(cross))]
    v_step_map = [[-1 for i in range(len(cross[0]))] for j in range(len(cross))]

    word_li = []  # Wordのインスタンスを保存する配列
    step = 0
    for j in range(H):
        for i in range(W):
            right = right_word(i, j, cross, W)
            if right:
                for k in range(len(right)):
                    h_step_map[j][i + k] = step
                step += 1
                word_li.append(Word(i, j, len(right), HORIZONTAL))

            down = down_word(i, j, cross, H)
            if down:
                for k in range(len(down)):
                    v_step_map[j + k][i] = step
                step += 1
                word_li.append(Word(i, j, len(down), VERTICAL))

    # Wordに隣接関係を追加する
    step = 0
    for j in range(H):
        for i in range(W):
            right = right_word(i, j, cross, W)
            if right:
                for k in range(len(right)):
                    if v_step_map[j][i + k] != -1:
                        word_li[step].add_next(v_step_map[j][i + k])
                step += 1

            down = down_word(i, j, cross, H)
            if down:
                for k in range(len(down)):
                    if h_step_map[j + k][i] != -1:
                        word_li[step].add_next(h_step_map[j + k][i])
                step += 1

    def recur(index, keys, coords=[]):
        """
        評価値が最大となるcoordsを取得する
        params:
            index:キーのうち何番目の文字か
            keys:キーとなっている文字の一覧
            corrds:鍵として確定した座標保存リスト(確定するごとに段々増えていく)
        """
        if index == len(keys):  # キーとなる文字のすべての座標が確定した場合
            for i in word_li:  # Wordの鍵対応一覧を取得
                i.check_is_key(coords)  # 鍵の文字数を更新する

            # 再帰的にWordのnextに飛んでis_keyが1以上のWordまでの最短距離を出す
            distance = 0
            for idx, i in enumerate(word_li):
                done = [idx]  # すでにチェックした単語の保存(自分自身がgetkeyの時にループが発生しておかしくなるのを防ぐ)
                if not i.get_is_key():  # キーが含まれていない単語は考慮する必要なし
                    continue

                next = i.get_next()  # 隣の単語一覧を取得
                while True:
                    distance += 1
                    next_temp = []  # 隣の隣の単語を保存する
                    fin = False
                    for j in next:  # 隣の単語をすべてチェックする
                        if not (j in done):  # 一度チェックしたやつは無視する
                            next_temp += word_li[j].get_next()
                            if word_li[j].get_is_key():
                                fin = True
                                break
                    if fin:
                        break
                    done += next
                    done = list(set(done))
                    if len(done) == len(word_li):
                        distance = 0
                        break
                    next = next_temp
            return distance, coords
        max_value = -1
        max_coords = []
        for i in itertools.combinations(
            coord_dic[keys[index]], word_dic[keys[index]]
        ):  # キーの文字座標から必要な文字数だけ座標を取得する
            ret, ret_c = recur(index + 1, keys, coords + list(i))
            if ret > max_value:  # 評価値が最も大きいやつを残して上の層に渡す
                max_value = ret
                max_coords = ret_c
        return max_value, max_coords

    value, coords = recur(0, list(coord_dic.keys()))
    return value, coords


def search_word(word, folderpath, H, W, threshold=0):
    """
    params:
        word:答えの単語
        folderpath:盤面データベースのフォルダパス
        H:クロスワードの高さ
        W:クロスワードの幅
        threshold:答えの分布の評価値の閾値
    """
    word_dic = {}
    for i in word:
        word_dic[i] = word_dic.get(i, 0) + 1

    files = os.listdir(folderpath)
    ret = []
    for i in files:
        with open(os.path.join(folderpath, i), "r", encoding="utf-8") as f:
            for cross_map in tqdm(f):
                if H * W != len(cross_map.split(",")):
                    raise Exception("cross_mapとサイズが異なります")

                # クロスワードのデータを2次元配列化
                cross = []
                line = []
                for i in cross_map.strip().split(","):
                    line.append(i)
                    if len(line) == W:
                        cross.append(list(line))
                        line = []

                # クロスワードに使用されている文字のカウント
                mozi_dic = {}
                for row in cross:
                    for item in row:
                        mozi_dic[item] = mozi_dic.get(item, 0) + 1

                # 使用されている文字で足りないものがあればmatch_flagをfalseにする
                match_flag = True
                for i in word_dic.keys():
                    if word_dic[i] > mozi_dic.get(i, 0):
                        match_flag = False

                # 使用されている文字数が必要数よりも多い場合は評価を行う。
                if match_flag:
                    value, coord = validate(word, cross)
                    if value >= threshold:
                        ret.append([cross, value, coord])
    return ret


if __name__ == "__main__":
    word = "かかし"  # キーとしたい単語
    filepath = os.path.join("test_data", "pokemon_1008_7_7")  # クロスワードデータベースを指定
    H = 7  # クロスワードの高さ
    W = 7  # クロスワードの幅
    threshold = 0  # 評価値の閾値
    save_number = 0  # 保存したいNo(0だと探索を行う)
    save_name = os.path.join("test_data", "to_product_test.txt")  # save_number指定時のファイル名

    ret = search_word(word, filepath, H, W, threshold)

    for i, j in enumerate(ret):
        if save_number:
            if save_number == i + 1:
                save_string = ""
                save_string += str(H) + "," + str(W) + "\n"
                for k in j[0]:
                    save_string += ",".join(k) + "\n"
                for k in j[2]:
                    save_string += str(k[0]) + "," + str(k[1]) + "\n"

                with open(save_name, "w", encoding="utf-8") as f:
                    f.write(save_string)
                print("save No.{}".format(i + 1))

        else:
            print("No.{}".format(i + 1))
            print("value:{} coords:{}".format(j[1], j[2]))
            for k in j[0]:
                for l in k:
                    print(l + ",", end="")
                print()
            print()
