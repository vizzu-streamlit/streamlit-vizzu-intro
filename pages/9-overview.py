import pandas as pd
import streamlit as st
import numpy as np
from ipyvizzu.animation import Config, Data, Style
from typing import List

from streamlit_vizzu import VizzuChart

data_frame = pd.read_csv("data/football_transfers_cleaned.csv", dtype={"year": str})

data = Data()
data.add_df(data_frame, max_rows=25000)

chart = VizzuChart(rerun_on_click=True, key="vizzu1", height=400)

# -- set default Style
style =  Style(
        {
            "plot": {
                "xAxis": {"label": {"numberScale": "shortScaleSymbolUS", "angle":"-1.1","fontSize": "0.9em",}},
				"yAxis": {"label": {"numberScale": "shortScaleSymbolUS"},"title":{"color":"#00000000"}},
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
            },
			"legend": {"width": "20em"},
})

chart.animate(data, style)
chart.feature("tooltip", True)

# -- select time range --
year1, year2 = st.select_slider(
    "Time range", options=map(str, np.arange(1992, 2023)), value=("1998", "2018")
)
filter_transfers = f"record['fee[m€]'] > 0"
filter_year = f"record['year'] >= {year1} && record['year'] <= {year2}"

#select clubs
defaultClubs = ['Arsenal FC', 'Chelsea FC', 'Liverpool FC', 'Manchester City', 'Manchester United']

selected_clubs: List[str] = st.multiselect('Clubs',options=data_frame.sort_values(by="club_name").club_name.unique(),default=['Arsenal FC', 'Chelsea FC', 'Liverpool FC', 'Manchester City', 'Manchester United'])

filter_clubs = (
    "(" + " || ".join([f"record['club_name'] == '{item}'" for item in selected_clubs]) + ")"
)

col1, col2, col3, col4, col5 = st.columns(5)

#select compared value
compare_by = col1.radio("Compare by", ["Fees earned", "Fees spent", "Balance"], index=1)
if compare_by == "Fees earned":
	compare_title = "Transfer fees earned "
	y = "fee[m€]"
	filter_value = "record.transfer_movement == 'out' && record.dummy == 'No'"
elif compare_by == "Fees spent":
	compare_title = "Transfer fees spent"
	y = "fee[m€]"
	filter_value = "record.transfer_movement == 'in' && record.dummy == 'No'"
else:
	compare_title = "Balance of transfer fees"
	y = "fee_real[m€]"
	filter_value = "record.transfer_movement != 'kiskalap' && record.dummy == 'No'" 
	
#set split or stack
split = col2.radio("Show clubs", ["Stacked","Side by side"], index=1)
if split == "Stacked":
	split_set = False
else:
	split_set = True
	
# -- concat filters --
filter = " && ".join([filter_value, filter_clubs,filter_year,filter_transfers])

# -- zoom to selected year and club
year_clicked = chart.get("marker.categories.year")
club_clicked = chart.get("marker.categories.club_name")

if year_clicked is None:
	chart.animate(
		Data.filter(filter),
		Config(
			{"x": "year", 
			"y": [y,"club_name"], 
			"color": "club_name",
			"geometry": "rectangle",
			"label": None,
			"split": split_set,
			"title": f"{compare_title}"},
		),
		delay = 0,
	)
else:
	filter_year2 = f"record['year'] == '{year_clicked}'"
	filter_club2 = f"record['club_name'] == '{club_clicked}'"
	filter2 = " && ".join([filter, filter_year2, filter_club2])
	chart.animate(Data.filter(filter2))
	chart.animate(
		Config({
			"x": y,
			"y": ["player_name","year"],
			"color" : "club_name",
			"sort": "byValue",
			"split": False,
			"label": y
		})
	)

chart.show()
