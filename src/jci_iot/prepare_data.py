import glob
import warnings
from pathlib import Path

import pandas as pd
from tqdm.auto import tqdm

warnings.filterwarnings("ignore")

data_location = "data/*.csv"
processed_data_fname = "data/processed_master.csv"
aggregated_data_fname = "data/aggregated_master.csv"


def load_data():
    processed_data = Path(processed_data_fname)
    if processed_data.is_file():
        # file exists
        data = pd.read_csv(processed_data)
        print(f"File exists. Loaded {processed_data}")
    else:
        data = pd.DataFrame()
        print(f"Generating processed data...")
        for file_ in tqdm(glob.glob(data_location)):
            df = pd.read_csv(file_, skiprows=5)
            df["playerid"] = file_[-6:-4]
            df["datetime"] = df["time[ISO-UTC]"].apply(
                lambda x: pd.to_datetime(f"{x.replace('T','')[:-3]}.{x[-3:]}", format="%Y%m%d%H%M%S.%f")
            )
            df["t"] = df["datetime"].dt.time
            df["s[m]"] = df["speed[km/h]"] * 0.1 / 3.6  # time taken is 100 ms = 0.1s
            df["a[m/s2]"] = (df["speed[km/h]"] / 3.6).diff() / 0.1
            df = df[df['a[m/s2]']>-8]
            data = pd.concat([data, df])
            # print(f"{file_}: {df.shape[0]} rows | data: {data.shape[0]} rows")

        data.to_csv("data/processed_master.csv")

    print(data.shape)
    # print(data.head())

    # load a player's data
    # preprocess it
    # generate aggs and store separate also
    # use individual data for individual plots

    aggregated_data = Path(aggregated_data_fname)
    if aggregated_data.is_file():
        # file exists
        player_aggs = pd.read_csv(aggregated_data)
        aggs_FH = pd.read_csv("data/aggs_FH.csv")
        aggs_SH = pd.read_csv("data/aggs_SH.csv")
        print(f"File exists. Loaded {aggregated_data}")

    else:

        print(f"Generating aggregated data...")
        player_aggs = get_aggs(data)
        aggs_FH = get_aggs(data.loc[data.datetime < "2018-10-31 19:30:00"])
        aggs_SH = get_aggs(data.loc[data.datetime > "2018-10-31 19:30:00"])

        player_aggs.to_csv("data/aggregated_master.csv", index=False)
        aggs_FH.to_csv("data/aggs_FH.csv", index=False)
        aggs_SH.to_csv("data/aggs_SH.csv", index=False)


    print(player_aggs.shape)
    # print(player_aggs.head())

    # return data, player_aggs, aggs_FH, aggs_SH


def get_aggs(data):
    player_ids = data.playerid.unique()
    player_aggs = pd.DataFrame()

    for i, p in tqdm(enumerate(player_ids)):
        pdf = data.query("playerid==@p").set_index("datetime", drop=True)
        player_aggs.loc[i, "player_id"] = p

        # x = pdf.last_valid_index() - pdf.first_valid_index()
        #     print (x)
        #     player_aggs.loc[i,'time_played'] = datetime.time(x.seconds//3600,x.seconds//60//60,x.seconds%60)
        player_aggs.loc[i, "time_played"] = pdf.shape[0] * 0.1 / 60  # x.seconds/60

        pdf["s[m]"] = pdf["speed[km/h]"] * 0.1 / 3.6  # time taken is 100 ms = 0.1s
        player_aggs.loc[i, "Distance[km]"] = pdf["s[m]"].sum() / 1000

        player_aggs.loc[i, "High_Intensity_Distance[km]"] = (
            pdf.loc[pdf["speed[km/h]"] > 15, ["s[m]"]].values.sum() / 1000
        )
        player_aggs.loc[i, "Distance[km]_[0-15 km/h]"] = pdf.loc[pdf["speed[km/h]"] < 15, ["s[m]"]].values.sum() / 1000
        player_aggs.loc[i, "Distance[km]_[15-20 km/h]"] = (
            pdf.loc[pdf["speed[km/h]"].between(15, 19, inclusive=True), ["s[m]"]].values.sum() / 1000
        )
        player_aggs.loc[i, "Distance[km]_[20-25 km/h]"] = (
            pdf.loc[pdf["speed[km/h]"].between(20, 24, inclusive=True), ["s[m]"]].values.sum() / 1000
        )
        player_aggs.loc[i, "Distance[km]_[25-20 km/h]"] = (
            pdf.loc[pdf["speed[km/h]"].between(25, 30, inclusive=True), ["s[m]"]].values.sum() / 1000
        )
        player_aggs.loc[i, "Distance[km]_[30+ km/h]"] = pdf.loc[pdf["speed[km/h]"] > 30, ["s[m]"]].values.sum() / 1000
        player_aggs.loc[i, "#sprints_[25+ km/h]"] = pdf.loc[pdf["speed[km/h]"] > 25].shape[0]

        player_aggs.loc[i, "Avg_Speed[km/h]"] = pdf["speed[km/h]"].mean()
        player_aggs.loc[i, "Max_Speed[km/h]"] = pdf["speed[km/h]"].max()

        pdf["a[m/s2]"] = (pdf["speed[km/h]"] / 3.6).diff() / 0.1
        player_aggs.loc[i, "acc_max[m/s2]"] = pdf["a[m/s2]"].max()
        player_aggs.loc[i, "#acc>3m/s2"] = pdf.loc[pdf["a[m/s2]"] > 3].shape[0]
        player_aggs.loc[i, "#acc>4m/s2"] = pdf.loc[pdf["a[m/s2]"] > 4].shape[0]
        player_aggs.loc[i, "#dec>3m/s2"] = pdf.loc[pdf["a[m/s2]"] < -3].shape[0]
        player_aggs.loc[i, "#dec>4m/s2"] = pdf.loc[pdf["a[m/s2]"] < -4].shape[0]

        player_aggs.loc[i, "HR_min[bpm]"] = pdf["hr[bpm]"].min()
        player_aggs.loc[i, "HR_max[bpm]"] = pdf["hr[bpm]"].max()
        player_aggs.loc[i, "HR_mean[bpm]"] = pdf["hr[bpm]"].mean()

        # HR Zones
        #     player_aggs.loc[i,'mins_in_HR_Zone_1'] = pdf['hr[bpm]'].between(110, 131, inclusive = True).astype(int).sum()*0.1/60
        #     player_aggs.loc[i,'mins_in_HR_Zone_2'] = pdf['hr[bpm]'].between(132, 153, inclusive = True).astype(int).sum()*0.1/60
        #     player_aggs.loc[i,'mins_in_HR_Zone_3'] = pdf['hr[bpm]'].between(154, 175, inclusive = True).astype(int).sum()*0.1/60
        #     player_aggs.loc[i,'mins_in_HR_Zone_4'] = pdf['hr[bpm]'].between(176, 197, inclusive = True).astype(int).sum()*0.1/60
        #     player_aggs.loc[i,'mins_in_HR_Zone_5'] = pdf['hr[bpm]'].between(198, 219, inclusive = True).astype(int).sum()*0.1/60

        #     Zone	    Intensity	Percentage of HRmax
        #     Zone 1	Very light	50–60%
        #     Zone 2	Light	    60–70%
        #     Zone 3	Moderate	70–80%
        #     Zone 4	Hard	    80–90%
        #     Zone 5	Maximum	    90–100%

        player_aggs.loc[i, "mins_in_HR_Zone_1"] = (
            pdf["hr[bpm]"]
            .between(pdf["hr[bpm]"].max() * 0.5, pdf["hr[bpm]"].max() * 0.6, inclusive=True)
            .astype(int)
            .sum()
            * 0.1
            / 60
        )
        player_aggs.loc[i, "mins_in_HR_Zone_2"] = (
            pdf["hr[bpm]"]
            .between(pdf["hr[bpm]"].max() * 0.6, pdf["hr[bpm]"].max() * 0.7, inclusive=True)
            .astype(int)
            .sum()
            * 0.1
            / 60
        )
        player_aggs.loc[i, "mins_in_HR_Zone_3"] = (
            pdf["hr[bpm]"]
            .between(pdf["hr[bpm]"].max() * 0.7, pdf["hr[bpm]"].max() * 0.8, inclusive=True)
            .astype(int)
            .sum()
            * 0.1
            / 60
        )
        player_aggs.loc[i, "mins_in_HR_Zone_4"] = (
            pdf["hr[bpm]"]
            .between(pdf["hr[bpm]"].max() * 0.8, pdf["hr[bpm]"].max() * 0.9, inclusive=True)
            .astype(int)
            .sum()
            * 0.1
            / 60
        )
        player_aggs.loc[i, "mins_in_HR_Zone_5"] = (
            pdf["hr[bpm]"].between(pdf["hr[bpm]"].max() * 0.9, pdf["hr[bpm]"].max(), inclusive=True).astype(int).sum()
            * 0.1
            / 60
        )

    return player_aggs


load_data()