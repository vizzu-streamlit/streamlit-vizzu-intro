import pandas as pd
import streamlit as st
from ipyvizzu.animation import Config, Data, Style

from streamlit_vizzu import VizzuChart

data_frame = pd.read_csv("data/football_transfers_cleaned.csv", dtype={"year": str})

data = Data()
data.add_df(data_frame, max_rows=25000)

chart = VizzuChart(key="vizzu", height=600)
chart.animate(data)
chart.feature("tooltip", True)

year = st.slider("Pick a year", min_value=1992, max_value=2022, value=2010)
col1, col2, col3, col4, col5 = st.columns(5)

compare_by = col1.radio("Compare by", ["Fees earned", "Fees spent", "Balance"], index=2)
if compare_by == "Fees earned":
	compare_title = "Transfer fees earned in "
	x = "fee[m€]"
	filter = f"record.year == '{year}' && record.transfer_movement == 'out' && record.dummy == 'No'"
elif compare_by == "Fees spent":
	compare_title = "Transfer fees spent in "
	x = "fee[m€]"
	filter = f"record.year == '{year}' && record.transfer_movement == 'in' && record.dummy == 'No'"
else:
	compare_title = "Balance of transfer fees in "
	x = "fee_real[m€]"
	filter = f"record.year == '{year}' && record.dummy == 'No'" 
	
order_by = col2.radio("Order by", ["Value","Alphabet"])
if order_by == "Value":
	sort = "byValue"
	reverse = False
else:
	sort = "none"
	reverse = True


chart.animate(
    Data.filter(filter),
    Config(
        {"x": x, 
		"y": "club_name", 
		"color": "club_name",
		"label": x,
		"sort": sort,
		"reverse": reverse,
		"title": f"{compare_title}{year}"}
    ),
    Style(
        {
            "plot": {
                "xAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                "marker": {
                    "colorPalette": (
                        "#EF0107 #FEE505 #ff0000 #034694 #007711 #1B458F #003399 #ea6a28 #7b7979 #C8102E #6CABDD #EF3829 #e11b22 #FCED0B #d4af37 #3c64d7 #ff33cc #0D171A #303030 #D71920 #132257 #ffff00 #000000 #dc161b #F3D459 #EDBB00 #000040 #bbbbda #fd1220 #ff0000 #0055ff #61584c #FBEE23 #00065d #103bce #007020 #000000 #231F20 #ffee00 #d72635 #feae37 #761ec8 #6C1D45 #ff5f00 #8a0829 #ccff00 #000000 #FFCD00 #192552 #3e2415"
                    ),
                    "label": {
                        "numberFormat": "prefixed",
                        "maxFractionDigits": "1",
                        "numberScale": "shortScaleSymbolUS",
                    },
                },
                "paddingLeft": "13em",
            }
        }
    ),
    delay = 0,
	#duration=0.2,
    x={"easing": "linear", "delay": 0},
    y={"delay": 0},
    show={"delay": 0},
    hide={"delay": 0},
    title={"duration": 0, "delay": 0},
)

chart.show()
