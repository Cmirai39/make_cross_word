

def make_words_list(cross_map:list,H:int,W:int):
    """
    鍵一覧を作る
    params:
        cross_map:2次元配列のクロスワード
        H:高さ
        W:幅
    ret:
        v_words:縦方向の単語一覧[(x,y,単語,問題ナンバー),...]
        h_words:横方向の単語一覧[(x,y,単語,問題ナンバー),...]
    """

    def right_word(x,y,cross_map,W):
        """
        右側に言葉があるかどうかを確認する
        あれば、その言葉を返す
        params:
            x:スタートのx座標
            y:スタートのy座標
            cross_map:クロスワードの盤面の2次元配列
            W:クロスワードの盤面の幅
        """

        if x>=1 and cross_map[y][x-1] != "黒":
            return ""
        
        i = 0
        ret = ""
        while True:
            if x+i < W:
                if cross_map[y][x+i] == "黒":
                    break
                else:
                    ret += cross_map[y][x+i]
                i += 1
            else:
                break
        
        if i == 0 or i == 1:
            return ""
        else:
            return ret
    
    def down_word(x,y,cross_map,H):
        """
        下側に言葉があるかどうかを確認する
        あれば、その言葉を返す
        params:
            x:スタートのx座標
            y:スタートのy座標
            cross_map:クロスワードの盤面の2次元配列
            H:クロスワードの盤面の高さ
        """
        if y>=1 and cross_map[y-1][x] != "黒":
            return ""
        i = 0
        ret = ""
        while True:
            if y+i < H:
                if cross_map[y+i][x] == "黒":
                    break
                else:
                    ret += cross_map[y+i][x]
                i += 1
            else:
                break
        if i == 0 or i == 1:
            return ""
        else:
            return ret
        
    v_words = [] #縦方向の単語一覧
    h_words = [] #横方向の単語一覧

    count = 0
    for j in range(H):
        for i in range(W):
            right = right_word(i,j,cross_map,W)
            down = down_word(i,j,cross_map,H)
            if right or down:
                count += 1
                if down:
                    v_words.append((i,j,down,count))
                if right:
                    h_words.append((i,j,right,count))
       
    return v_words,h_words