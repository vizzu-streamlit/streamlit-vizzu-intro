import pandas as pd
import streamlit as st
from streamlit_vizzu import Config, Data, VizzuChart

st.set_page_config(page_title="Intro to Streamlit-Vizzu", page_icon="🚀")

chart = VizzuChart()

df = pd.DataFrame({"cat": ["x", "y", "z"], "val": [1, 2, 3]})
data = Data()
data.add_df(df)
chart.animate(data)

st.subheader(
    "Visit [intro-to-vizzu-in.streamlit.app](https://intro-to-vizzu-in.streamlit.app/)"
)

chart.animate(Config({"x": "cat", "y": "val", "title": "Look at my plot!"}))

if st.checkbox("Swap"):
    chart.animate(Config({"x": "val", "y": "cat", "title": "Swapped!"}))

output = chart.show()

if output and "data" in output and "values" in output["data"]:
    st.write("value of clicked bar:", output["data"]["values"]["val"])

st.caption("Data shown on the chart")
st.dataframe(df)
