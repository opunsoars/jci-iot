import pandas as pd
import plotly.graph_objects as go

data = pd.read_csv("data/processed_master.csv")
player_aggs = pd.read_csv("data/aggregated_master.csv")
aggs_FH = pd.read_csv("data/aggs_FH.csv")
aggs_SH = pd.read_csv("data/aggs_SH.csv")


# choose player
p = "02"
pdf = data.query("playerid==@p").set_index(["datetime"])
pdf["acc_class"] = "default"
pdf.loc[pdf["a[m/s2]"] > 3, "acc_class"] = "#acc>3m/s2"
pdf.loc[pdf["a[m/s2]"] > 4, "acc_class"] = "#acc>4m/s2"
pdf.loc[pdf["a[m/s2]"] < -3, "acc_class"] = "#dec>3m/s2"
pdf.loc[pdf["a[m/s2]"] < -4, "acc_class"] = "#dec>4m/s2"


# conditions
fh_filter = pdf.index < "2018-10-31 19:30:00"
sh_filter = pdf.index > "2018-10-31 19:30:00"


# traces individual
speed = go.Scatter(x=pdf.index, y=pdf["speed[km/h]"], mode="lines", name="speed[km/h]", connectgaps=False, xaxis="x")
distance = go.Scatter(x=pdf.index, y=pdf["s[m]"], mode="lines", name="distance[m]", connectgaps=False, xaxis="x")
# cum overlay
total_distance = go.Scatter(
    x=pdf.index,
    y=pdf["s[m]"].cumsum(),
    mode="lines",
    name="total distance[m]",
    connectgaps=False,
    fill="tozeroy",
    xaxis="x2",
)

acc = go.Scatter(x=pdf.index, y=pdf["a[m/s2]"], mode="lines", name="acceleration[m/s2]", connectgaps=False, xaxis="x")
hr = go.Scatter(x=pdf.index, y=pdf["hr[bpm]"], mode="lines", name="heart-rate[bpm]", connectgaps=False, xaxis="x")

# total dis | bandwise dis (hor stack) [1/2/total]
# sprint count [1/2/total]| swarm plot with sprints highlight
# acc bands background , swarm overlay, avg/max/min (do 1/2 on timeseries)

sel_cols = aggs_FH.columns[4:9]
banded_distance_FH = go.Bar(
    y=sel_cols,
    x=list(aggs_FH.query("player_id==@p")[sel_cols].values.flatten()),
    name="FH",
    orientation="h",
    # marker=dict(
    #     color='rgba(246, 78, 139, 0.6)',
    #     line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
    # )
)
sel_cols = aggs_SH.columns[4:9]
banded_distance_SH = go.Bar(
    y=sel_cols,
    x=list(aggs_SH.query("player_id==@p")[sel_cols].values.flatten()),
    name="SH",
    orientation="h",
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

# acc bands stack bar
sel_cols = ["#dec>4m/s2", "#dec>3m/s2", "#acc>3m/s2", "#acc>4m/s2"]
banded_acc = go.Bar(
    x=player_aggs.query("player_id==@p")[sel_cols].to_dict("split")["columns"],
    y=player_aggs.query("player_id==@p")[sel_cols].to_dict("split")["data"][0],
    name="bandwise_accelerations",
    orientation="v",
    # marker=dict(
    #     color='rgba(246, 78, 139, 0.6)',
    #     line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
    # )
)

# sprints scatter

sprints = go.Scatter(
    x=pdf.query("playerid==@p").loc[pdf["speed[km/h]"] > 25, "speed[km/h]"].index,
    y=pdf.query("playerid==@p").loc[pdf["speed[km/h]"] > 25, "speed[km/h]"].values,
    mode="markers",
    marker=dict(size=5, color="yellow", symbol="star", line=dict(width=1, color="DarkSlateGrey")),
    name="sprints",
    # connectgaps=False,
    xaxis="x",
)

# HR two periods hist overlap
hr_fh = pdf.query("playerid==@p").loc[fh_filter, "hr[bpm]"].dropna().values
hist_data = [hr_fh]
group_labels = ["FH BPM"]
if p != "16":
    hr_sh = pdf.query("playerid==@p").loc[sh_filter, "hr[bpm]"].dropna().values

    hist_data = [hr_fh, hr_sh]
    group_labels = ["FH BPM", "SH BPM"]


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
