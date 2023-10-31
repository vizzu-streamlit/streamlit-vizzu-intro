import pandas as pd
import streamlit as st
import numpy as np
from ipyvizzu.animation import Config, Data, Style
from typing import List

from streamlit_vizzu import VizzuChart

data_frame = pd.read_csv("data/football_transfers_cleaned.csv", dtype={"year": str})

data = Data()
data.add_df(data_frame, max_rows=25000)

chart = VizzuChart(key="positions", height=400)

# -- set default Style
style =  Style(
        {
            "plot": {
                "xAxis": {"label": {"numberScale": "shortScaleSymbolUS", "fontSize": "0.9em",}},
				"yAxis": {"label": {"numberScale": "shortScaleSymbolUS"},"title":{"color":"#00000000"}},
                "marker": {
                    "colorPalette": (
						"#00ff00 #00ff00 #6cabdd #000000 #ff0000 #00ff00 #ff0000 #000000 #00ff00 #000000 #ff0000 #ff0000 #000000 #00ff00 #ff0000 #00ff00"
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
    "Time range", options=map(str, np.arange(1992, 2023)), value=("1992", "2022")
)
filter_year = f"record['year'] >= {year1} && record['year'] <= {year2}"

# -- filter only transfers coming in
filter_dir = "record.transfer_movement == 'in' && record.dummy == 'No'"

#select clubs
defaultClubs = ['Arsenal FC', 'Chelsea FC', 'Liverpool FC', 'Manchester City', 'Manchester United']

selected_clubs: List[str] = st.multiselect('Clubs',options=data_frame.sort_values(by="club_name").club_name.unique(),default=['Arsenal FC', 'Chelsea FC', 'Liverpool FC', 'Manchester City', 'Manchester United'])

filter_clubs = (
    "(" + " || ".join([f"record['club_name'] == '{item}'" for item in selected_clubs]) + ")"
)

col1, col2, col3, col4, col5 = st.columns(5)

#select compared value
compare_by = col1.radio("Compare by", ["Transfer fees", "Count of transfers"])
if compare_by == "Transfer fees":
	compare_title = "Average of transfer fees"
	y = "mean(fee[m€])"
	filter_transfers = f"record['fee[m€]'] > 0"
else:
	compare_title = "Count of transfers"
	y = "count()"
	filter_transfers = f"record['fee[m€]'] >= 0"
	
# -- concat filters --
filter = " && ".join([filter_year,filter_transfers,filter_dir])

# -- zoom to selected year and club
year_clicked = chart.get("marker.categories.year")
club_clicked = chart.get("marker.categories.club_name")

chart.animate(
	Data.filter(filter),
	Config(
		{"x": "mean(age)",
		"y": y, 
		"color": "position",
		"geometry": "circle",
		"label": None,
		"noop":["year"]
	}),
	delay = 0,
)

chart.show()
