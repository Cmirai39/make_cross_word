# 実行手順
## search_cross.pyによるプロダクト生成用ファイルの作成
初めにsearch_cross.pyを実行して、クロスワードの盤面データから作りたい条件を満たすクロスワードを探します。
```bash
python3 search_cross.py
```
これを実行して、お望みにクロスワードを見つけたら、save_numberに指定してあげて、もう一度```python3 search_cross.py```を実行すると、to_product.txtというファイルが生成されます。<br>
search_cross.pyで変更するのは以下で示した部分です。
```python
word = "かかし"  # キーとしたい単語
filepath = os.path.join("test_data", "pokemon_1008_7_7")  # クロスワードデータベースを指定
H = 7  # クロスワードの高さ
W = 7  # クロスワードの幅
threshold = 0  # 評価値の閾値
save_number = 0  # 保存したいNo(0だと探索を行う)
save_name = "to_product.txt"  # save_number指定時のファイル名
```
wordは最後に出来上がる言葉を指定することができます。<br>
filepathはクロスワードの盤面のデータファイルを指定します。今回は、テストとして、ポケモンの名前のみで構成された7x7マスのクロスワード300個を用意しています(本来は何万個もあります)。クロスワードの高さや幅はクロスワードのデータがほかにもある場合に変更することができます。テストデータでは7x7から変更することはできません。<br>
thresholdは表示されるクロスワードを評価値がthreshold以上のクロスワードに制限することができます。より広い範囲にキーが分散したクロスワードを探したい場合にこの値を高くしてください。<br>
save_numberは保存したい番号を指定します。まず、初めに0を指定して条件を満たすクロスワードを探索すると、No.がついたクロスワードが表示されてきます。このNo.を覚えておき, save_numberにそのNo.を入力することで、指定したNo.のクロスワードのproduct生成用ファイルを保存することができます。<br>
save_nameは、save_numberを指定したときに、生成するproduct生成用ファイルの名前を指定できます。

## to_product.pyによるプロダクトの作成
search_cross.pyによって出力されたファイルを元に画像を生成します。
```bash
python3 to_product.py
```
これを実行するとproductフォルダの配下にtestというフォルダの下に画像と問題番号とその答えのテキストファイルが作成されます。
これを元にお好みのクロスワードを作成してください。
to_product.pyで変更するのは以下で示した部分です。
```
# 入力指定
path = os.path.join("test_data", "to_product_test.txt")  # search_cross.pyの出力ファイルを指定
description_path = os.path.join("test_data", "test_dic.json")# 単語の説明ファイルを指定

# 成果物のファイル名指定
product_name = "test"  # 成果物を保存するフォルダ名
q_png_name = "img_q_test.png"  # 問題用画像生成ファイル名
a_png_name = "img_a_test.png"  # 解答用画像生成ファイル名
v_word_name = "key_v.txt"  # 縦の鍵一覧番号生成ファイル名
h_word_name = "key_h.txt"  # 横の鍵一覧番号生成ファイル名
description_name = "description.png"  # ヒント文生成画像ファイル名
``````
pathはsearch_cross.pyから出力されたファイルを指定します。<br>
description_pathは単語とそのヒント文を書いたファイルを指定します。ファイルはjsonで、以下のようにフォーマットにしたがって書きます。
```
{
    "テスト":"学習の結果を評価するために行われるもの",
    "期末テスト":"テストの中でも学期の終わりに行われるもの"
}
```

# 補足
クロスワードの盤面データは2次元配列を1次元配列に直し、改行で1つ1つのクロスワードを表しています。
```
クロスワード1の盤面
クロスワード2の盤面
        .
        .
```
盤面データは現在配布していません。<br>
今後、無料配布または有料配布を考えています。
配布と同時に、本プログラムのGUI版の作成も予定しているのでご期待ください。
本プログラムを用いて作成したクロスワードは[X(twitter)](https://twitter.com/B45Wb7KRlJuxHed)で公開しています。
