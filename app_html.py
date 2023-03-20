import streamlit as st
import streamlit.components.v1 as components
import openai
import time
import numpy as np

openai.api_key = st.secrets['api_key']

HEADER = '''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <style>
* { box-sizing: border-box; }
table { margin: 10px; }
tr:first-child td {
	border-top: 2px solid lightgray;
}
tr:nth-child(3n) td {
	border-bottom: 2px solid lightgray;
}
td {
	border: 1px solid white;
	height: 80px;
	width: 80px;
	text-align: center;
    word-wrap: break-word;
}
td:first-child {
	border-left: 2px solid lightgray;
}
td:nth-child(3n) {
	border-right: 2px solid lightgray;
}
td.inner {
	background-color: aqua;
}
td.outer {
	background-color: white;
}
td.center {
	background-color: aqua;
	font-weight: bold;
}
</style>
    <title>マンダラート</title>
</head>
<body>
'''
FOOTER  = '</body>\n</html>'
SP4 = "    "

MANDAL_LIST = [[ 9, 10, 11, 18, 19, 20, 27, 28, 29],
               [12, 13, 14, 21, 22, 23, 30, 31, 32],
               [15, 16, 17, 24, 25, 26, 33, 34, 35],
               [36, 37, 38,  0,  1,  2, 45, 46, 47],
               [39, 40, 41,  3,  4,  5, 48, 49, 50],
               [42, 43, 44,  6,  7,  8, 51, 52, 53],
               [54, 55, 56, 63, 64, 65, 72, 73, 74],
               [57, 58, 59, 66, 67, 68, 75, 76, 77],
               [60, 61, 62, 69, 70, 71, 78, 79, 80]]

st.set_page_config(
    page_title = "ＡＩマンダラート",
#     page_icon = Image.open("favicon.png")
)

def association_words(word, temp, NG_words=[""]):
    prompt_txt = f"""Answer 10 japanese keywords without NG words that you associate with this word. Answer should be Japanese:

# word: {word}

# NG words: {str([NG_words])[1:-1]}

# format: Python list style with single quotation

Anser:
"""
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_txt,
        temperature=temp,
        max_tokens=500,
        top_p=1.0,
        frequency_penalty=0.8,
        presence_penalty=0.0
    )
    res = response.choices[0].text
    result = res.replace("’", "'").replace("‘", "'").replace(";", "")
    return eval(result)

def get_class_name(num):
    result = ""
    result += "inner" if num < 9 else "outer"
    result += " center"  if num in range(4, 81, 9) else ""
    return result

def create_mandalachart(title, type_AI):
    if type_AI == 'きっちり':
        temp = 0.0
    elif type_AI == 'まぁまぁ':
        temp = 0.5
    else: # 'クリエイティブ'
        temp = 0.9
# AI association word
    words_dic, NG_list = dict(), [title]
    words = association_words(title, temp, NG_list)[:8]
    words_dic[title] = words
    NG_list = words[:]
    for word in words:
        time.sleep(1)
        ass_words = association_words(word, temp, NG_list)[:8]
        words_dic[word] = ass_words
        NG_list += ass_words
# data arrange
    blocks = list()
    for key, words in words_dic.items():
        words.insert(4, key)
        blocks.append(words)
# html create
    html, csv = f'{HEADER}<table id="mandal"><tbody>\n', ''
    for row in MANDAL_LIST:
        html += f'{SP4*1}<tr>\n'
        class_name = ""
        for num in row:
            class_name = get_class_name(num)
            blk_row, blk_col = num // 9, num % 9
            html += f'{SP4*2}<td class="{class_name}">{blocks[blk_row][blk_col]}</td>\n'
            csv += f"'{blocks[blk_row][blk_col]}', "
        html += f'{SP4*1}</tr>\n'
        csv = csv[:-2] + "\n"
    html += f'</tr></tbody></table>\n{FOOTER}'
    return html, csv

# layout
st.header("ＡＩが創るマンダラート")

title = st.text_input("**お題を入力してください :**")
type_AI = st.radio(
    "**どのＡＩに創らせますか :**",
    ('きっちり', 'まぁまぁ', 'クリエイティブ'), horizontal=True)

mandala_html, mandala_csv = "", ""
if st.button('**マンダラート創造**') and title:
    try:
        with st.spinner("マンダラート創造中・・・30秒～数分程度お待ちください。"):
            mandala_html, mandala_csv = create_mandalachart(title, type_AI)
            components.html(mandala_html, width=800, height=850)
    except Exception as err:
        st.error(f'エラーが発生しました。再度お試し下さい。', icon="🚨") #\n({err=}, {type(err)=}

if mandala_html:
    st.download_button(
        label="CSVダウンロード【ダウンロードするとマンダラートは消えます】",
        data=mandala_csv,
        file_name='mandalachart.csv',
        mime='text/csv',
    )
