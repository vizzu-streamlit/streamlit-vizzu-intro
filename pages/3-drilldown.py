import pandas as pd
import streamlit as st
from streamlit_vizzu import Config, Data, Style, VizzuChart

chart = VizzuChart(rerun_on_click=True, default_duration=1, height=380)

data_frame = pd.read_csv("data/music.csv", dtype={"Year": str})

data = Data()
data.add_df(data_frame)

style = Style(
    {
        "plot": {
            "xAxis": {"label": {"angle": "-1.1"}},
            "yAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
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

handler = '''
let Year = parseFloat(event.data.text);
if (!isNaN(Year) && Year > 1950 && Year < 2020 && Year % 5 !== 0) {
    event.preventDefault();
}
'''

# Add handler to the plot-axis-label-draw event
chart.on('plot-axis-label-draw', handler)

chart.feature("tooltip", True)

bar_clicked = chart.get("target.categories.Year")

if bar_clicked is None:
    chart.animate(data, style)
    chart.animate(
        Data.filter(),
        Config(
            {
                "x": "Year",
                "y": "Revenue[$]",
                "sort": "none",
                "color": None,
                "label": None,
                "title": "Music Revenues",
            }
        ),
        style,
        delay="0",
    )
else:
    chart.animate(Data.filter(f"record['Year'] == '{bar_clicked}' && record['Revenue[$]'] !== 0"))
    chart.animate(
        Config.groupedColumn(
            {
                "x": "Format",
                "y": "Revenue[$]",
                "groupedBy": "Format",
                "sort": "byValue",
                "title": f"Drilldown for Year {bar_clicked}",
            }
        )
    )

chart.show()

"Click on one of the bars to see the drilldown"
