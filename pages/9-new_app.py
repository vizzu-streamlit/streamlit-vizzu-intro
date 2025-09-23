from streamlit_vizzu import VizzuChart, Data, Config, Style
import pandas as pd
import streamlit as st
from typing import List

d_types = {
    "Year": str,
    "Quarter": str,
    "Continent": str,
    "Country": str,
    "Category": str,
    "Sub-Category": str,
    "Items sold": float,
    "Unit price[$]": float,
    "Revenue[$]": float,
    "Profit[$]": float,
}
df = pd.read_csv("data/sales.csv", dtype=d_types)
data = Data()
data.add_df(df)

chart = VizzuChart()
chart.feature("tooltip", True)
chart.animate(data)

col1, col2 = st.columns([1, 3])
if col1.checkbox('Reorder'):
    x= ['Year', 'Quarter']
else:
    x= ['Quarter', 'Year']

items: List[str] = col2.multiselect(
    "Quarters", ["Q1", "Q2", "Q3", "Q4"],["Q1", "Q2", "Q3", "Q4"], key="multiselect"
)

filter = (
    "(" + " || ".join([f"record['Quarter'] == '{item}'" for item in items]) + ")"
)

chart.animate(
    Data.filter(filter),
    Config(
        {
            "coordSystem": "cartesian",
            "geometry": "rectangle",
            "x": x,
            "y": {"set": "Items sold", "range": {"min": "auto", "max": "110%"}},
            "color": "Quarter",
            "lightness": None,
            "size": None,
            "noop": None,
            "split": False,
            "align": "none",
            "orientation": "horizontal",
            "label": None,
            "sort": "none",
            "legend":'color',
        }
    ),
    Style(
        {
            "plot": {
                "yAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                "xAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                "marker": {
                    "label": {
                        "numberFormat": "prefixed",
                        "maxFractionDigits": "1",
                        "numberScale": "shortScaleSymbolUS",
                    },
                    "rectangleSpacing": None,
                    "circleMinRadius": 0.005,
                    "borderOpacity": 1,
                    "colorPalette": "#03ae71 #f4941b #f4c204 #d49664 #f25456 #9e67ab #bca604 #846e1c #fc763c #b462ac #f492fc #bc4a94 #9c7ef4 #9c52b4 #6ca2fc #5c6ebc #7c868c #ac968c #4c7450 #ac7a4c #7cae54 #4c7450 #9c1a6c #ac3e94 #b41204",
                },
            }
        }
    ),
)

chart.show()