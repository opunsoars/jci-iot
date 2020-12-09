import numpy as np
import plotly.graph_objects as go

# from src.jci_iot.prepare_data import load_data

# data, player_aggs = load_data()

# # choose player
# p = "02"
# pdf = data.query("playerid==@p").set_index(["datetime"])

# # time = pdf["t"]
# speed = pdf["speed[km/h]"]
# distance = pdf["s[m]"]
# acc = pdf["a[m/s2]"]
# hr = pdf["hr[bpm]"]

# speed_1 = go.Scatter(x=pdf.index, y=pdf.loc[pdf.index<'2018-10-31 19:30:00',"speed[km/h]"], mode="lines", name="speed[km/h] - half I")
# distance_1 = go.Scatter(x=pdf.index, y=pdf.loc[pdf.index<'2018-10-31 19:30:00',"s[m]"], mode="lines", name="distance[m] - half I")
# acc_1 = go.Scatter(x=pdf.index, y=pdf.loc[pdf.index<'2018-10-31 19:30:00',"a[m/s2]"], mode="lines", name="acceleration[m/s2] - half I")
# hr_1 = go.Scatter(x=pdf.index, y=pdf.loc[pdf.index<'2018-10-31 19:30:00',"hr[bpm]"], mode="lines", name="heart-rate[bpm] - half I")

# speed_2 = go.Scatter(x=pdf.index, y=pdf.loc[pdf.index>'2018-10-31 19:30:00',"speed[km/h]"], mode="lines", name="speed[km/h] - half II")
# distance_2 = go.Scatter(x=pdf.index, y=pdf.loc[pdf.index>'2018-10-31 19:30:00',"s[m]"], mode="lines", name="distance[m] - half II")
# acc_2 = go.Scatter(x=pdf.index, y=pdf.loc[pdf.index>'2018-10-31 19:30:00',"a[m/s2]"], mode="lines", name="acceleration[m/s2] - half II")
# hr_2 = go.Scatter(x=pdf.index, y=pdf.loc[pdf.index>'2018-10-31 19:30:00',"hr[bpm]"], mode="lines", name="heart-rate[bpm] - half II")

# np.random.seed(1)

# N = 100
# random_x = np.linspace(0, 1, N)
# random_y0 = np.random.randn(N) + 5
# random_y1 = np.random.randn(N)
# random_y2 = np.random.randn(N) - 5

# fig = go.Figure()

# # Add traces
# # fig.add_trace(go.Scatter(x=time, y=distance, mode="markers", name="distance"))
# # fig.add_trace(go.Scatter(x=time, y=speed, mode="lines+markers", name="speed"))
# fig.add_trace(go.Scatter(x=pdf.index, y=acc, mode="lines", name="acceleration"))

# fig.show()


from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
from traces import *

fig_svaHR = make_subplots(
    rows=4,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.02,
)

fig_svaHR.add_trace(hr, row=1, col=1)
fig_svaHR.add_trace(acc, row=2, col=1)
fig_svaHR.add_trace(distance, row=3, col=1)
fig_svaHR.add_trace(speed, row=4, col=1)
fig_svaHR.add_trace(sprints, row=4, col=1)


# fig_svaHR.add_trace(banded_acc, row=2, col=2)
# fig_svaHR.update_layout(barmode="stack")
# fig_svaHR.add_trace(total_distance, row=3, col=2)
# fig_svaHR.add_trace(banded_distance_FH, row=4, col=2)
# fig_svaHR.add_trace(banded_distance_SH, row=4, col=2)


# Update yaxis properties
fig_svaHR.update_yaxes(title_text=hr["name"], row=1, col=1)
fig_svaHR.update_yaxes(title_text=acc["name"], row=2, col=1)
fig_svaHR.update_yaxes(title_text=distance["name"], row=3, col=1)
fig_svaHR.update_yaxes(title_text=speed["name"], row=4, col=1)
fig_svaHR.update_xaxes(
    showspikes=True,
    spikemode="across",
    spikesnap="cursor",
    showline=True,
    showgrid=False,
)
fig_svaHR.update_layout(
    height=800,
    width=800,
    title_text="Stacked Subplots with Shared X-Axes",
    showlegend=False,
    hovermode="x",
    spikedistance=-1,
)
fig_svaHR.update_layout(barmode="stack")
fig_svaHR.update_layout(annotations=half_annos)
# fig_svaHR.show()

# # Add range slider
# fig.update_layout(
#     xaxis4=dict(
#         rangeselector=dict(
#             # buttons=list([
#             #     dict(count=1,
#             #          label="1m",
#             #          step="month",
#             #          stepmode="backward"),
#             #     dict(count=6,
#             #          label="6m",
#             #          step="month",
#             #          stepmode="backward"),
#             #     dict(count=1,
#             #          label="YTD",
#             #          step="year",
#             #          stepmode="todate"),
#             #     dict(count=1,
#             #          label="1y",
#             #          step="year",
#             #          stepmode="backward"),
#             #     dict(step="all")
#             # ])
#         ),
#         rangeslider=dict(visible=True),
#         type="date",
#     )
# )
fig_banded_dis = go.Figure()
fig_banded_dis.add_trace(banded_distance_FH)
fig_banded_dis.add_trace(banded_distance_SH)
fig_banded_dis.update_layout(
    barmode="stack",
    legend=dict(
        x=0.6,
        y=0.8,
        traceorder="reversed",
    ),
)
fig_banded_dis.update_layout(height=300, width=400, margin=dict(l=0, r=0, t=20, b=0))
fig_banded_dis.update_layout(annotations=dis_band_anno)

# banded accelerations
fig_banded_acc = go.Figure()
fig_banded_acc.add_trace(banded_acc)
fig_banded_acc.update_layout(
    barmode="stack",
    # legend=dict(
    #     x=0.6,
    #     y=0.8,
    #     traceorder="grouped+reversed",
    # ),
)
fig_banded_acc.update_layout(height=300, width=400, margin=dict(l=0, r=0, t=20, b=0))
# fig_banded_acc.update_layout(annotations=dis_band_anno)


fig_HR_dist = ff.create_distplot(hist_data, group_labels, bin_size=5, show_rug=False, histnorm= '')
fig_HR_dist.update_layout(height=300, width=400, margin=dict(l=0, r=0, t=20, b=0), legend=dict(x=0.1, y=0.9))


# banded HR
fig_banded_HR = go.Figure()
for trace in banded_HR_traces:
    fig_banded_HR.add_trace(trace)
fig_banded_HR.update_layout(barmode="stack")
fig_banded_HR.update_layout(height=300, width=400, margin=dict(l=0, r=0, t=20, b=0), legend=dict(x=0.1, y=0.95, orientation='h'))
fig_banded_HR.update_layout(annotations=[anno_HR])