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

st.set_page_config(
    page_title = "ＡＩマンダラート",
#     page_icon = Image.open("favicon.png")
)

def association_words(word, temp, NG_words=[""]):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Answer 8 japanese keywords without NG words that you associate with this word:\n\nword: {word}\n\nNG words: {str([NG_words])[1:-1]}\n\nformat: Python list\n\nAnser:",
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
    if num < 9:
        result += "inner"
    else:
        result += "outer"

    if num in range(4, 81, 9):
        result += " center"
    return result

def create_mandalachart(title, type_AI):
    if type_AI == 'きっちり':
        temp = 0.1
    elif type_AI == 'まぁまぁ':
        temp = 0.5
    else: # 'クリエイティブ'
    temp = 0.9
# AI
    words_dic, NG_list = dict(), list()
    words = association_words(KEYWORD, temp, NG_list)[:8]
    words_dic[KEYWORD] = words
    NG_list = words[:]
    for word in words:
        time.sleep(1)
        ass_words = association_words(word, temp, NG_list)[:8]
        words_dic[word] = ass_words
        NG_list += ass_words
# data arrange
    num_key = {num: word for  num, word in enumerate(words_dic)}
    blocks = list()
    for num, key in num_key.items():
        temp = list()
        for idx, word in enumerate(words_dic[key]):
            if idx == 3:
                temp += [word, key]
            else:
                temp += [word]
        blocks.append(temp)
# data arrange mandarchart
    mdl = np.array([num for num in range(81)])
    mdl = mdl.reshape(9, 9)
    upper = np.concatenate([mdl[1].reshape(3,3), mdl[2].reshape(3,3), mdl[3].reshape(3,3)], 1)
    middle = np.concatenate([mdl[4].reshape(3,3), mdl[0].reshape(3,3), mdl[5].reshape(3,3)], 1)
    lower = np.concatenate([mdl[6].reshape(3,3), mdl[7].reshape(3,3), mdl[8].reshape(3,3)], 1)
    mandal = np.concatenate([upper, middle, lower])
# html create    
    html = f'{HEADER}<table id="mandal"><tbody>\n'
    for row in mandal:
        html += f'{SP4*1}<tr>\n'
        class_name = ""
        for num in row:
            class_name = get_class_name(num)
            blk_row, blk_col = num // 9, num % 9
            html += f'{SP4*2}<td class="{class_name}">{blocks[blk_row][blk_col]}</td>\n'
        html += f'{SP4*1}</tr>\n'
    html += f'</tr></tbody></table>\n{FOOTER}'
    return html

# layout
st.header("ＡＩが創るマンダラート")

title = st.text_input("**お題を入力してください :**")
type_AI = st.radio(
    "**どのＡＩに創らせますか :**",
    ('きっちり', 'まぁまぁ', 'クリエイティブ'), horizontal=True)
if st.button('**マンダラート創造**'):
    try:
        with st.spinner("マンダラート創造中・・・"):
            components.html(title, type_AI, width=800, height=800)
    except:
        st.error('エラーが発生しました。再度お試し下さい', icon="🚨")
