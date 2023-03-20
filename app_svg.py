import streamlit as st
import streamlit.components.v1 as components
import openai
import time
import numpy as np
import string
import base64

st.set_page_config(
    page_title = "ＡＩマンダラート",
#     page_icon = Image.open("favicon.png")
)

# OPEN AI API KEY
openai.api_key = st.secrets['api_key']

# Mandal Chart Layout
ROW, COL, UNIT = 9, 9, 80
MANDAL_LIST = [[ 9, 10, 11, 18, 19, 20, 27, 28, 29],
               [12, 13, 14, 21, 22, 23, 30, 31, 32],
               [15, 16, 17, 24, 25, 26, 33, 34, 35],
               [36, 37, 38,  0,  1,  2, 45, 46, 47],
               [39, 40, 41,  3,  4,  5, 48, 49, 50],
               [42, 43, 44,  6,  7,  8, 51, 52, 53],
               [54, 55, 56, 63, 64, 65, 72, 73, 74],
               [57, 58, 59, 66, 67, 68, 75, 76, 77],
               [60, 61, 62, 69, 70, 71, 78, 79, 80]]

# Cart Back Ground Color C0: default, C1: center, C2: center group, c3: outer_center
C0, C1, C2, C3 = "white", "pink", "aqua", "aqua"
COLOR = {(4, 4): C1, (3, 3): C2, (3, 4): C2, (3, 5): C2, (4, 3): C2, (4, 5): C2, (5, 3): C2, (5, 4): C2, (5, 5): C2,
         (1, 1): C3, (1, 4): C3, (1, 7): C3, (4, 1): C3, (4, 7): C3, (7, 1): C3, (7, 4): C3, (7, 7): C3}

# AI type : temperature
AI_TYPE = {'きっちり': 0.0, 'まぁまぁ': 0.5, 'クリエイティブ': 0.9}

# SVG TEMPLATE
SVG_HEADER = '''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 720 720">
<style>
    div { display: table; font-size: 16px; color: black; width: 70px; height: 80px; }
    p   { display: table-cell; text-align: center; vertical-align: middle;}
</style>
'''
SVG_ITEM = string.Template('''<g transform="translate($x,$y)">
    <rect x="0" y="0" width="80" height="80" fill="$color" stroke="gray"/>
    <foreignObject x="5" y="0" width="70" height="80">
       <body xmlns="http://www.w3.org/1999/xhtml"><div><p><text>$word</text></p></div></body>
    </foreignObject>
</g>
''')
SVG_FRAME = string.Template('''<g transform="translate($x,$y)">
    <rect x="0" y="0" width="$unit3" height="$unit3" fill="white" fill-opacity="0.0" stroke="black"/>
</g>
''')

# API PROMPT
PROMPT = string.Template('''Answer 10 japanese keywords without NG words that you associate with this word. Answer should be Japanese:

# word: $WORD

# NG words: $NG_WORD

# format: Python list style with single quotation

Anser:
''')

def association_words(word, temp, NG_words=[""]):
    prompt_txt = PROMPT.safe_substitute({
                    'WORD': word,
                    'NG_WORD': str([NG_words])[1:-1]
                 })
    
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

def create_mandalachart(title, type_AI):
    temp = AI_TYPE[type_AI]
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
# create SVG
    svg = SVG_HEADER
    for y, row in enumerate(MANDAL_LIST):
        for x, num in enumerate(row):
            word = blocks[num // COL][num % COL]
            color = COLOR.get((x, y), C0)
            svg += SVG_ITEM.safe_substitute({
                'x': x * UNIT, 'y': y * UNIT,
                'word': word,
                'color': color,
            })

    unit3 = UNIT * 3
    for x, y in ((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)):
        svg += SVG_FRAME.safe_substitute({
            'x': x * unit3, 'y': y * unit3, 'unit3': unit3
        })
    svg += '</svg>'
    return svg

# layout
st.header("ＡＩが創るマンダラート")

title = st.text_input("**お題を入力してください :**")
type_AI = st.radio("**どのＡＩに創らせますか :**",
                   ('きっちり', 'まぁまぁ', 'クリエイティブ'), horizontal=True)

mandala_svg, mandala_svg_output = "", ""
if st.button('**マンダラート創造**') and title:
    try:
        with st.spinner("マンダラート創造中・・・　数分程度お待ちください。"):
            mandala_svg = create_mandalachart(title, type_AI)
            components.html(mandala_svg, height=720)
    except Exception as err:
        st.error(f'エラーが発生しました。　　再度お試し下さい。')
        st.error(f'{err=}, {type(err)=}')
