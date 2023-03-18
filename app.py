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
	border-top: 4px solid darkgrey;
}
tr:nth-child(3n) td {
	border-bottom: 4px solid darkgrey;
}
td {
	border: 1px solid lightgrey;
	height: 80px;
	width: 80px;
	text-align: center;
    word-wrap: break-word;
}
td:first-child {
	border-left: 4px solid darkgrey;
}
td:nth-child(3n) {
	border-right: 4px solid darkgrey;
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
'''
FOOTER  = '</body>\n</html>'
SP4 = "    "

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
    if num < 9:
        result += "inner"
    else:
        result += "outer"

    if num in range(4, 81, 9):
        result += " center"
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
# data arrange mandala
    mdl = np.array([num for num in range(81)])
    mdl = mdl.reshape(9, 9)
    upper = np.concatenate([mdl[1].reshape(3,3), mdl[2].reshape(3,3), mdl[3].reshape(3,3)], 1)
    middle = np.concatenate([mdl[4].reshape(3,3), mdl[0].reshape(3,3), mdl[5].reshape(3,3)], 1)
    lower = np.concatenate([mdl[6].reshape(3,3), mdl[7].reshape(3,3), mdl[8].reshape(3,3)], 1)
    mandal = np.concatenate([upper, middle, lower])
# html create
    html = f'{HEADER}<table id="mandal"><tbody>\n'
    csv = ""
    for row in mandal:
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
        with st.spinner("マンダラート創造中・・・１分程度お待ちください。"):
            mandala_html, mandala_csv = create_mandalachart(title, type_AI)
            components.html(mandala_html, width=800, height=800)
    except Exception as err:
        st.error(f'エラーが発生しました。再度お試し下さい。({err=}, {type(err)=}', icon="🚨")

if mandala_html:
    st.download_button(
        label="CSVダウンロード【ダウンロードするとマンダラートは消えます】",
        data=mandala_csv,
        file_name='mandalachart.csv',
        mime='text/csv',
    )
