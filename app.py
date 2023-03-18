import streamlit as st
import streamlit.components.v1 as components
# import openai
# from PIL import Image

# layout
st.header("ＡＩが創るマンダラート")

title = st.text_input("**お題を入力してください :**")
temp = st.radio(
    "どのＡＩに創らせますか",
    ('きっちり', 'まぁまぁ', 'クリエイティブ'), horizontal=True)
if st.button('マンダラート創造'):
    pass

components.html('''
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <style>
* { box-sizing: border-box; }
table { margin: 10px; }
tr:first-child td {
	border-top-color: black;
}
tr:nth-child(3n) td {
	border-bottom-color: black;
}
td {
	border: 1px solid lightgrey;
	height: 80px;
	width: 80px;
	text-align: center;
    word-wrap: break-word;
}
td:first-child {
	border-left-color: black;
}
td:nth-child(3n) {
	border-right-color: black;
}
td.inner {
	background-color: aqua;
}
td.center {
	background-color: aqua;
	font-weight: bold;
}    
</style>
    <title>マンダラート</title>
</head>
<body>
<table id="mandal"><tbody>
    <tr>
        <td class="outer">イノベーション</td>
        <td class="outer">開発</td>
        <td class="outer">リリース</td>
        <td class="outer">トレンド</td>
        <td class="outer">最先端</td>
        <td class="outer">最新技術</td>
        <td class="outer">議論</td>
        <td class="outer">会話</td>
        <td class="outer">コミュニケーション</td>
    </tr>
    <tr>
        <td class="outer">試作品</td>
        <td class="outer center">新製品</td>
        <td class="outer">プレミアム</td>
        <td class="outer">モダン</td>
        <td class="outer center">最新</td>
        <td class="outer">アップデート</td>
        <td class="outer">ディスカッション</td>
        <td class="outer center">話題</td>
        <td class="outer">意見交換</td>
    </tr>
    <tr>
        <td class="outer">高性能</td>
        <td class="outer">ハイテク</td>
        <td class="outer">マーケティング</td>
        <td class="outer">アップグレード</td>
        <td class="outer">イノベーティブ</td>
        <td class="outer">パワフル</td>
        <td class="outer">熱談</td>
        <td class="outer">交流</td>
        <td class="outer">ネタバレ</td>
    </tr>
    <tr>
        <td class="outer">人気急上昇</td>
        <td class="outer">大人気</td>
        <td class="outer">熱狂的な支持</td>
        <td class="inner">新製品</td>
        <td class="inner">最新</td>
        <td class="inner">話題</td>
        <td class="outer">限定版</td>
        <td class="outer">限定品</td>
        <td class="outer">限定数量</td>
    </tr>
    <tr>
        <td class="outer">大勢の人々</td>
        <td class="outer center">人気</td>
        <td class="outer">注目度</td>
        <td class="inner">人気</td>
        <td class="inner center">新商品</td>
        <td class="inner">限定</td>
        <td class="outer">特別版</td>
        <td class="outer center">限定</td>
        <td class="outer">オリジナル</td>
    </tr>
    <tr>
        <td class="outer">話題性</td>
        <td class="outer">流行り</td>
        <td class="outer">ヒット作</td>
        <td class="inner">早い者勝ち</td>
        <td class="inner">特別価格</td>
        <td class="inner">購入</td>
        <td class="outer">レア</td>
        <td class="outer">コレクターズ・アイテム</td>
        <td class="outer">コレクション</td>
    </tr>
    <tr>
        <td class="outer">迅速</td>
        <td class="outer">競争</td>
        <td class="outer">早押し</td>
        <td class="outer">割引</td>
        <td class="outer">セール</td>
        <td class="outer">特価</td>
        <td class="outer">ショッピング</td>
        <td class="outer">購入者</td>
        <td class="outer">購入物</td>
    </tr>
    <tr>
        <td class="outer">即効性</td>
        <td class="outer center">早い者勝ち</td>
        <td class="outer">スピード感</td>
        <td class="outer">値下げ</td>
        <td class="outer center">特別価格</td>
        <td class="outer">安い</td>
        <td class="outer">商品</td>
        <td class="outer center">購入</td>
        <td class="outer">価格</td>
    </tr>
    <tr>
        <td class="outer">緊張感</td>
        <td class="outer">勝負心</td>
        <td class="outer">先取り</td>
        <td class="outer">お得</td>
        <td class="outer">割安</td>
        <td class="outer">特別オファー</td>
        <td class="outer">決済</td>
        <td class="outer">クレジットカード</td>
        <td class="outer">オンラインショップ</td>
    </tr>
</tr></tbody></table>
</body>
</html>
    ''',
    width=800, height=800)
