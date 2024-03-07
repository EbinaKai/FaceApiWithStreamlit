import io
import requests
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from PIL import ImageDraw, ImageFont
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)
dotenv_path = join(dirname('__file__'), '.env')
subscription_key = os.environ.get("AZURE_KEY")

# API情報
assert subscription_key
face_api_url = 'https://20220220ebi.cognitiveservices.azure.com/face/v1.0/detect'

st.title('Face Recognition App')

uploaded_file = st.file_uploader("Shoose an image...", type=['jpeg','jpg','png','JPEG','PNG'])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    
    # 画像をバイナリデータに変換
    with io.BytesIO() as output:
        img.save(output, format='JPEG')
        binary_img = output.getvalue()
        
    # APIに送信
    headers = {
        "Content-Type": "application/octet-stream",
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    params = {
        'returnFaceId': 'true',
        'returnFaceAttributes': 'age,gender',
    }
    
    res = requests.post(face_api_url, params=params, headers=headers, data=binary_img)
    results = res.json()
    if not results:
        st.write('画像から顔を検出できませんでした。')
    else :
        # BBを描画
        for result in results:
            rect = result['faceRectangle']
            atter = result['faceAttributes']

            
            
            draw = ImageDraw.Draw(img)
            draw.rectangle(
                [(rect['left'], rect['top']),
                (rect['left']+rect['width'], rect['top']+rect['height'])],
                fill=None,
                outline='blue',
                width=5
            )
            
            caption = atter['gender']+', age:'+str(atter['age'])
            font = ImageFont.truetype("/System/Library/Fonts/AppleSDGothicNeo.ttc", size=40)
            position = (rect['left']+10, rect['top']-40)
            draw.text(position, caption, 'white', font=font)

    # 画像を表示
    st.image(img, caption='Uploaded image', use_column_width=True)