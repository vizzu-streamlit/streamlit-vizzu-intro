import pandas as pd
import streamlit as st
from streamlit_vizzu import Config, Data, VizzuChart

###############################################################################
# Header of page
###############################################################################
st.set_page_config(layout="wide", page_title="Data Editor and Vizzu", page_icon="🧮")
c1, c2 = st.columns([2, 1])
c1.header("Editable dataframes and Vizzu charts")
warning_placeholder = st.empty()

###############################################################################
# Adding new columns to the dataframe
###############################################################################
st.subheader("My Pokedex (editable table)")
with st.expander("Add new columns to the dataframe?"):
    st.write(
        """To add a new column to the dataframe, fill the fields below and click on the button.
    The new column will be added to the dataframe and the visualization options will be updated
    if the new column is not on the current dataframe columns.
    """
    )
    c1, c2, c3, c4 = st.columns(4)
    st.caption("Add a new column to the dataframe")
    col_name = c1.text_input("Column name", "new_col")
    dtype_sel = c2.selectbox("Data type", ["float", "str"])
    if dtype_sel == "float":
        default_value = c3.number_input("Default Value", 0)
    elif dtype_sel == "str":
        default_value = c3.text_input("Default Value", "empty")
    else:
        default_value = None
    c4.markdown("")
    c4.markdown("")
    add_sel = c4.button("Add column to dataframe")

###############################################################################
# Editable dataframe
###############################################################################
if "current_df" not in st.session_state:
    initial_df = pd.DataFrame(
        {
            "pokemon": ["Bulbasaur", "Charmander", "Pikachu", "Rattata", "Snorlax"],
            "type": ["Plant", "Fire", "Electric", "?", "?"],
            "active": [False, True, True, True, False],
            "# pokemons": [1, 2, 1, 10, 1],
            "attack": [1, 2, 1, 10, 1],
        }
    )
    st.session_state.current_df = initial_df

new_col_required = (
    add_sel and col_name != "" and col_name not in st.session_state.current_df.columns
)
if add_sel and col_name != "" and col_name not in st.session_state.current_df.columns:
    st.session_state.current_df[col_name] = [
        default_value for _ in range(len(st.session_state.current_df))
    ]
    # st.session_state.current_df = initial_df
    # st.experimental_rerun()

edited_df = st.data_editor(
    st.session_state.current_df,
    use_container_width=True,
    num_rows="dynamic",
    column_config={
        "active": st.column_config.CheckboxColumn(default=True),
        "# pokemons": st.column_config.NumberColumn(default=1),
    },
)
st.caption(
    "If not familiar with how to work with editable dataframes, check the [documentation](http://docs.streamlit.io/library/advanced-features/dataframes#edit-data-with-stdata_editor)."
)

###############################################################################
# Plot options
###############################################################################
st.subheader("Visualization options")
c1, c2 = st.columns([1, 1])
graph_sel = c1.selectbox("Type of graph", ["Grouped Column", "Pie", "Bubble"])
agg_sel = c2.selectbox(
    "Type of aggregation on graph", ["sum", "min", "max", "count", "distinct"]
)
st.session_state.graph_type = graph_sel
st.session_state.graph_agg = agg_sel

###############################################################################
# Getting input from users
###############################################################################
str_cols = list(edited_df.select_dtypes(include=["object"]).columns)
num_cols = list(edited_df.select_dtypes(include=["float", "int"]).columns)
c1, c2, c3, c4 = st.columns(4)
if graph_sel == "Grouped Column":
    x_sel = c1.selectbox("x", str_cols)
    y_sel = c2.selectbox("y", num_cols)
    color_sel = c3.selectbox("color", num_cols)
elif graph_sel == "Pie":
    by_sel = c1.selectbox("by", str_cols)
    angle_sel = c2.selectbox("angle", num_cols)
    color_sel = c3.selectbox("color", str_cols)
elif graph_sel == "Bubble":
    color_sel = c1.selectbox("color", str_cols)
    size_sel = c2.selectbox("size", num_cols)
else:
    x_sel = c1.selectbox("x", str_cols)
    y_sel = c2.selectbox("y", num_cols)
    color_sel = c3.selectbox("color", str_cols)

###############################################################################
# The visualization
###############################################################################
# Clean the dataframe
if edited_df.isnull().values.sum() != 0:
    warning_placeholder.warning(
        "Rows with None, Null or NaN values will not be shown in the visualization."
    )
else:
    warning_placeholder.empty()
clean_df = edited_df.dropna()
# Create/Update the data - use the data stored in session_state as previous data
current_data = Data()
current_df = st.session_state.current_df
current_data.add_df(current_df[current_df["active"]])
edited_data = Data()
edited_data.add_df(clean_df[clean_df["active"]])
# Create the chart
chart = VizzuChart(width="100%")
# Additional options
# agg_y_sel = f"{agg_sel}({y_sel})"
# agg_y_sel_dict = {"channels": {"y": {"set": [agg_y_sel]}}}
# Select the plot type
if st.session_state.graph_type == "Grouped Column":
    config = Config.groupedColumn({"x": x_sel, "y": y_sel, "color": color_sel})
elif st.session_state.graph_type == "Pie":
    config = Config.pie({"by": by_sel, "angle": angle_sel, "color": color_sel})
elif st.session_state.graph_type == "Bubble":
    config = Config.bubble({"size": size_sel, "color": color_sel})
else:
    config = Config({"x": x_sel, "y": y_sel})
# Add the first chart
chart.animate(current_data)
chart.animate(config)
# Add the edited chart
chart.animate(edited_data)
chart.animate(config)

only_active = Data.filter("record['active'] == true")
chart.animate(only_active)

# Show
st.subheader("My Pokedex (Vizzu chart)")
chart.show()

# Update the dataframe
st.session_state.current_df = clean_df

# Some other links
_, c1, c2, c3 = st.columns([1, 2, 2, 2])
c1.caption(
    "[streamlit-vizzu documentation](https://github.com/vizzu-streamlit/streamlit-vizzu/)"
)
c2.caption("[streamlit documentation](https://docs.streamlit.io/)")
c3.caption("[(ipy)vizzu documentation](https://ipyvizzu.vizzuhq.com/latest/)")
