import streamlit as st
import pandas as pd
import requests

st.title("Pico_W_職能發展協會專案")
st.header("雞舍:red[溫度]和:blue[光線]狀態")
st.divider()

url = 'https://blynk.cloud/external/api/get?token=nzK-CMS_SCHp34fOZ46k_nwFqOEQu7Ws&v1&v2&v3&v4'

response = requests.request("GET",url)
if response.status_code == 200:
    all_data = response.json()
    st.info(f'Relay1:{all_data["v1"]}')
    st.warning(f'Relay2:{all_data["v2"]}')
    st.info(f'光線:{all_data["v3"]}')
    st.warning(f'可變電阻:{all_data["v4"]}')
else:
    st.write("連線失敗,請等一下再試")
