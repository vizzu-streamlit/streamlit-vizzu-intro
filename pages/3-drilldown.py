import pandas as pd
import streamlit as st
from streamlit_vizzu import Config, Data, Style, VizzuChart

st.set_page_config(page_title="Intro to Streamlit-Vizzu", page_icon="🚀")

chart = VizzuChart(rerun_on_click=True, default_duration=1, height=380)

data_frame = pd.read_csv("data/music.csv", dtype={"Year": str})

data = Data()
data.add_df(data_frame)

style = Style(
    {
        "plot": {
            "xAxis": {"label": {"angle": "-1.1"}},
            "yAxis": {
                "label": {
                    "numberFormat": "prefixed",
                    "numberScale": "shortScaleSymbolUS",
                }
            },
            "marker": {
                "colorPalette": (
                    "#b74c20FF #c47f58FF #1c9761FF #ea4549FF #875792FF #3562b6FF "
                    "#ee7c34FF #efae3aFF"
                ),
                "label": {
                    "numberFormat": "prefixed",
                    "maxFractionDigits": "1",
                    "numberScale": "shortScaleSymbolUS",
                },
            },
            "paddingLeft": "8em",
        },
    }
)

# Add handler
chart.on("plot-axis-label-draw", """
const year = Number.parseInt(event.detail?.text, 10);
if (Number.isFinite(year) && year > 1950 && year < 2020 && year % 5 !== 0) {
    event.preventDefault();
}
""")

chart.feature("tooltip", True)

bar_clicked = chart.get("target.categories.Year")

if bar_clicked is None:
    chart.animate(data, style)
    chart.animate(
        Data.filter(),
        Config(
            {
                "channels": {
                    "x": {"set": ["Year"]},
                    "y": {"set": ["Revenue[$]"]},
                    "color": {"set": []},
                    "label": {"set": []},
                    "size": {"set": []},
                    "lightness": {"set": []},
                },
                "geometry": "rectangle",
                "sort": "none",
                "title": "Music Revenues",
            }
        ),
        style,
        delay=0,
    )
else:
    chart.animate(Data.filter(f"record['Year'] == '{bar_clicked}' && record['Revenue[$]'] !== 0"))
    chart.animate(
        Config(
            {
                "channels": {
                    "x": {"set": ["Format"]},
                    "y": {"set": ["Revenue[$]"]},
                    "color": {"set": ["Format"]},
                    "label": {"set": ["Revenue[$]"]},
                    "size": {"set": []},
                    "lightness": {"set": []},
                },
                "geometry": "rectangle",
                "sort": "byValue",
                "title": f"Drilldown for Year {bar_clicked}",
            }
        )
    )

chart.show()

st.caption("Click on one of the bars to see the drilldown")
