import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
from plotly.subplots import make_subplots


data = pd.read_csv("data/processed_master.csv")
player_aggs = pd.read_csv("data/aggregated_master.csv")
aggs_FH = pd.read_csv("data/aggs_FH.csv")
aggs_SH = pd.read_csv("data/aggs_SH.csv")

players = data.playerid.unique()
available_indicators = player_aggs.columns

def get_updated_data(player):
    p = str(player)
    pdf = data.query("playerid==@p").set_index(["datetime"])
    pdf["acc_class"] = "default"
    pdf.loc[pdf["a[m/s2]"] > 3, "acc_class"] = "#acc>3m/s2"
    pdf.loc[pdf["a[m/s2]"] > 4, "acc_class"] = "#acc>4m/s2"
    pdf.loc[pdf["a[m/s2]"] < -3, "acc_class"] = "#dec>3m/s2"
    pdf.loc[pdf["a[m/s2]"] < -4, "acc_class"] = "#dec>4m/s2"

    fh_filter = pdf.index < "2018-10-31 19:30:00"
    sh_filter = pdf.index > "2018-10-31 19:30:00"

    # traces individual
    hr = go.Scatter(x=pdf.index, y=pdf["hr[bpm]"], mode="lines", name="heart-rate[bpm]", marker_color='#A93C33', xaxis="x")
    acc = go.Scatter(
        x=pdf.index, y=pdf["a[m/s2]"], mode="lines", name="acceleration[m/s2]", marker_color='#4F425A', xaxis="x"
    )
    distance = go.Scatter(x=pdf.index, y=pdf["s[m]"], mode="lines", name="distance[m]", marker_color='#568A85', xaxis="x")
    speed = go.Scatter(
        x=pdf.index, y=pdf["speed[km/h]"], mode="lines", name="speed[km/h]",marker_color='#2C6334', xaxis="x"
    )
    sprints = go.Scatter(
        x=pdf.loc[pdf["speed[km/h]"] > 25, "speed[km/h]"].index,
        y=pdf.loc[pdf["speed[km/h]"] > 25, "speed[km/h]"].values,
        mode="markers",
        marker=dict(size=7, color="gold", symbol="star", line=dict(width=0.5, color="red")),
        name="sprints",
        # connectgaps=False,
        xaxis="x",
    )

    half_annos = []
    acc_FH_max = dict(
        xref="x",
        yref="y2",
        x=pdf.loc[fh_filter, "a[m/s2]"].idxmax(),
        y=pdf.loc[fh_filter, "a[m/s2]"].max(),
        text=f"Max FH: {round(pdf.loc[fh_filter,'a[m/s2]'].max(),2)} m/s2",
        showarrow=True,
        arrowhead=1,
    )

    hr_FH_max = dict(
        xref="x",
        yref="y",
        x=pdf.loc[fh_filter, "hr[bpm]"].idxmax(),
        y=pdf.loc[fh_filter, "hr[bpm]"].max(),
        text=f"Max FH: {round(pdf.loc[fh_filter,'hr[bpm]'].max(),2)} BPM",
        showarrow=True,
        arrowhead=1,
    )

    half_annos.extend([acc_FH_max, hr_FH_max])

    if p != "16":
        acc_SH_max = dict(
            xref="x",
            yref="y2",
            x=pdf.loc[sh_filter, "a[m/s2]"].idxmax(),
            y=pdf.loc[sh_filter, "a[m/s2]"].max(),
            text=f"Max SH: {round(pdf.loc[sh_filter,'a[m/s2]'].max(),2)} m/s2",
            showarrow=True,
            arrowhead=1,
        )

        hr_SH_max = dict(
            xref="x",
            yref="y",
            x=pdf.loc[sh_filter, "hr[bpm]"].idxmax(),
            y=pdf.loc[sh_filter, "hr[bpm]"].max(),
            text=f"Max SH: {round(pdf.loc[sh_filter,'hr[bpm]'].max(),2)} BPM",
            showarrow=True,
            arrowhead=1,
        )

        half_annos.extend([acc_SH_max, hr_SH_max])

    fig_svaHR = make_subplots(
        rows=4,
        cols=1,
        shared_xaxes=True,
        # vertical_spacing=0.02,
    )

    fig_svaHR.add_trace(hr, row=1, col=1)
    fig_svaHR.add_trace(acc, row=2, col=1)
    fig_svaHR.add_trace(distance, row=3, col=1)
    fig_svaHR.add_trace(speed, row=4, col=1)
    fig_svaHR.add_trace(sprints, row=4, col=1)

    # Update yaxis properties
    fig_svaHR.update_yaxes(title_text=hr["name"], row=1, col=1)
    fig_svaHR.update_yaxes(title_text=acc["name"], row=2, col=1)
    fig_svaHR.update_yaxes(title_text=distance["name"], row=3, col=1)
    fig_svaHR.update_yaxes(title_text=speed["name"], row=4, col=1)

    # Update xaxis properties
    fig_svaHR.update_xaxes(
        showspikes=True,
        spikemode="across",
        spikesnap="cursor",
        showline=True,
        showgrid=False,
    )

    # update layout
    fig_svaHR.update_layout(
        height=600,
        width=800,
        # title_text="Stacked Subplots with Shared X-Axes",
        margin=dict(l=20, r=0, t=20, b=0),
        showlegend=False,
        hovermode="x",
        spikedistance=-1,
        barmode="stack",
        annotations=half_annos,
    )

    # -----------------------------------------------------------------------------------------------
    sel_cols = aggs_FH.columns[4:9]
    banded_distance_FH = go.Bar(
        y=sel_cols,
        x=list(aggs_FH.query("player_id==@p")[sel_cols].values.flatten()),
        name="1st half",
        orientation="h",
        marker_color='#376a78'
        # marker=dict(
        #     color='rgba(246, 78, 139, 0.6)',
        #     line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
        # )
    )
    sel_cols = aggs_SH.columns[4:9]
    banded_distance_SH = go.Bar(
        y=sel_cols,
        x=list(aggs_SH.query("player_id==@p")[sel_cols].values.flatten()),
        name="2nd half",
        orientation="h",
        marker_color='#eba628'
        # marker=dict(
        #     color='rgba(246, 78, 139, 0.6)',
        #     line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
        # )
    )

    dis_band_anno = []
    for y, x in zip(sel_cols, list(player_aggs.query("player_id==@p")[sel_cols].values[0])):
        dis_band_anno.append(
            dict(
                # xref="x2",
                # yref="y8",
                y=y,
                x=x + 1,
                text=str(round(x, 2)) + " km",
                font=dict(family="Arial", size=12, color="black"),
                showarrow=False,
            )
        )
    fig_banded_dis = go.Figure()
    fig_banded_dis.add_trace(banded_distance_FH)
    fig_banded_dis.add_trace(banded_distance_SH)
    fig_banded_dis.update_layout(
        title='<b>Distance (km) covered in speed bands</b>',
        barmode="stack",
        legend=dict(
            x=0.5,
            y=0.8,
            traceorder="reversed",
        ),
    )
    fig_banded_dis.update_layout(height=300, width=400, margin=dict(l=0, r=0, t=30, b=0))
    fig_banded_dis.update_layout(annotations=dis_band_anno)

    # acc bands stack bar
    sel_cols = ["#dec>4m/s2", "#dec>3m/s2", "#acc>3m/s2", "#acc>4m/s2"]
    colors = ['#de425b','#f0b8b8','#bad0af','#488f31']
    banded_acc = go.Bar(
        x=player_aggs.query("player_id==@p")[sel_cols].to_dict("split")["columns"],
        y=player_aggs.query("player_id==@p")[sel_cols].to_dict("split")["data"][0],
        name="bandwise_accelerations",
        orientation="v",
        marker_color=colors,
        # marker=dict(
        #     color='rgba(246, 78, 139, 0.6)',
        #     line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
        # )
    )

    fig_banded_acc = go.Figure()
    fig_banded_acc.add_trace(banded_acc)
    fig_banded_acc.update_layout(
        title='<b>Acceleration/Deceleration count in bands</b>',
        barmode="stack",
        # legend=dict(
        #     x=0.6,
        #     y=0.8,
        #     traceorder="grouped+reversed",
        # ),
    )
    fig_banded_acc.update_layout(height=300, width=400, margin=dict(l=0, r=0, t=30, b=0))

    # HR two periods hist overlap
    hr_fh = pdf.query("playerid==@p").loc[fh_filter, "hr[bpm]"].dropna().values
    hist_data = [hr_fh]
    group_labels = ["FH BPM"]
    if p != "16":
        hr_sh = pdf.query("playerid==@p").loc[sh_filter, "hr[bpm]"].dropna().values

        hist_data = [hr_fh, hr_sh]
        group_labels = ["FH BPM", "SH BPM"]

    fig_HR_dist = ff.create_distplot(hist_data, group_labels, bin_size=5, show_rug=False, histnorm="", colors=['#376a78','#eba628'])
    fig_HR_dist.update_layout(title='<b>HR(bpm) distribution in 1st/2nd half</b>',
    height=300, width=400, margin=dict(l=0, r=0, t=30, b=0), legend=dict(x=0.1, y=0.9))

    names = ["50-60% HRmax", "60-70% HRmax", "70-80% HRmax", "80-90% HRmax", "90-100% HRmax"]
    colors = ["#C79C3E", "#C7843E", "#C76D3E", "#C7553E", "#C73E3E"]
    band_values = player_aggs.query("player_id==@p").T[-5:].values
    banded_HR_traces = [
        go.Bar(
            y=["HR"],
            x=band_values[i],
            width=0.3,
            name=names[i],
            text=f"{round(band_values[i][0],1)}mins",
            marker_color=colors[i],
            orientation="h",
            # marker=dict(
            #     color='rgba(246, 78, 139, 0.6)',
            #     line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
            # )
        )
        for i in range(5)
    ]

    # display min/max/mean HR
    anno_HR = dict(
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.1,
        text=f"Min: {round(pdf['hr[bpm]'].min(),2)} BPM | Avg: {round(pdf['hr[bpm]'].mean(),2)} BPM | Max: {round(pdf['hr[bpm]'].max(),2)} BPM",
        font=dict(size=12),
        showarrow=False,
    )

    # banded HR
    fig_banded_HR = go.Figure()
    for trace in banded_HR_traces:
        fig_banded_HR.add_trace(trace)
    fig_banded_HR.update_layout(barmode="stack",title='<b>Mins spent in HR bands</b>',
        height=300, width=400, margin=dict(l=0, r=0, t=30, b=0), legend=dict(x=0.1, y=0.95, orientation="h")
    )
    fig_banded_HR.update_layout(annotations=[anno_HR])

    cols = [
        "time_played",
        "Distance[km]",
        "High_Intensity_Distance[km]",
        "#sprints_[25+ km/h]",
        "Avg_Speed[km/h]",
        "Max_Speed[km/h]",
        "acc_max[m/s2]",
        "HR_min[bpm]",
        "HR_max[bpm]",
        "HR_mean[bpm]",
    ]
    table = pd.concat(
        [
            aggs_FH.query("player_id==@p")[cols],
            aggs_SH.query("player_id==@p")[cols],
            player_aggs.query("player_id==@p")[cols],
        ]
    )
    table.index = ["First Half (FH)", "Second Half (SH)", "Full Time"]
    table.columns = [col.replace("_", " ") for col in table.columns]
    table = round(table, 2)
    table.rename(columns={"time played": "time played[mins]"}, inplace=True)

    info_table2 = dbc.Table.from_dataframe(
        table.reset_index(), bordered=True, dark=True, hover=True, responsive=True, striped=True, size="sm",# style={'width':'10rem'}
    )

    return fig_svaHR, fig_banded_dis, fig_banded_acc, fig_HR_dist, fig_banded_HR, info_table2


def get_player_data(player):
    p = str(player)
    pdf = data.query("playerid==@p").set_index(["datetime"])
    pdf["acc_class"] = "default"
    pdf.loc[pdf["a[m/s2]"] > 3, "acc_class"] = "#acc>3m/s2"
    pdf.loc[pdf["a[m/s2]"] > 4, "acc_class"] = "#acc>4m/s2"
    pdf.loc[pdf["a[m/s2]"] < -3, "acc_class"] = "#dec>3m/s2"
    pdf.loc[pdf["a[m/s2]"] < -4, "acc_class"] = "#dec>4m/s2"
    return pdf



# banded accelerations

# fig_banded_acc.update_layout(annotations=dis_band_anno)


# infotable
# table=table.iloc[:,:4].reset_index()
# table = table.reset_index()

# info_table = dash_table.DataTable(
#     id="table",
#     columns=[{"name": i, "id": i} for i in table.columns],
#     data=table.to_dict("records"),
#     sort_action="native",
#     # filter_action="native",
#     # style_cell=dict(textAlign="left"),
#     # style_header=dict(backgroundColor="paleturquoise"),
#     # style_data=dict(backgroundColor="lavender"),
#     # css={"rule": "display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit"},
#     # style_data={"whiteSpace": "normal"},
#     # style_cell_conditional=[{"if": {"row_index": "even"}, "backgroundColor": "#f9f9f9"}],
#     style_data_conditional=[{"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}],
#     style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
#     style_cell={
#         "padding": "0px",
#         "midWidth": "0px",
#         "width": "0%",
#         "font-family": "arial",
#         "font-size": "12px",
#         "textAlign": "center",
#         "border": "white",
#         "whiteSpace": "normal",
#         "height": "auto",
#         "maxWidth": "0",
#     },
#     # style_cell={
#     # },
# )
