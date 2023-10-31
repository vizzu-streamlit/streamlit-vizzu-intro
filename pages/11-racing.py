import pandas as pd
import streamlit as st
from ipyvizzu.animation import Config, Data, Style

from streamlit_vizzu import VizzuChart

data_frame = pd.read_csv("data/football_transfers_cleaned.csv", dtype={"year": str})

data = Data()
data.add_df(data_frame, max_rows=25000)

chart = VizzuChart(key="vizzu", height=500)

# -- set default Style
style =  Style(
        {
            "plot": {
                "paddingLeft":"13em",
				"xAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
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

for y in range(1992, 2022):
	chart.animate(
		Data.filter(f"record.year <= {y} && record.transfer_movement == 'in'"),	
		Config({
			"x": "fee[m€]", 
			"y": {"set":"club_name","range": {"min": "-9.99999max"}}, 		
			#"y":"club_name",
			"color": "club_name",
			"label": "fee[m€]",
			"sort":"byValue",
			"title": f"Total transfer fees spent up to {y}"
			}),
		delay = 0,
		duration=0.6,
		x={"easing": "linear", "delay": 0},
		y={"delay": 0},
		show={"delay": 0},
		hide={"delay": 0},
		title={"duration": 0, "delay": 0},
	)

chart.show()
