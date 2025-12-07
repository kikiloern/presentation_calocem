#%% Import Module
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from calocem import tacalorimetry 
from calocem.tacalorimetry import Measurement

# 122 Bernburg Referenz
# 345 Karlstadt Referenz
# 260, 259, 258, 257 Bernburg mit Citronensäure
# 347, 348, 349, 350 Karlstadt mit Citronensäure


# %% Dateipfade definieren
calodatapath = Path(__file__).parent.parent / 'presentation_calocem' /'data'
outputpath = Path(__file__).parent.parent / 'presentation_calocem' /'output'

# %% Messung laden
tam = Measurement(calodatapath, regex="JAA_CAL.*.csv")

group1_ids = ["122", "260", "259", "258", "257"]
group2_ids = ["345", "347", "348", "349", "350"]

regex_group1 = r"JAA_CAL(" + "|".join(group1_ids) + r")\.csv"
regex_group2 = r"JAA_CAL(" + "|".join(group2_ids) + r")\.csv"


regex_group1 = r"JAA_CAL(" + "|".join(group1_ids) + r")\.csv"
regex_group2 = r"JAA_CAL(" + "|".join(group2_ids) + r")\.csv"

tam_g1 = Measurement(calodatapath, regex=regex_group1)
tam_g2 = Measurement(calodatapath, regex=regex_group2)

# %%
fig, ax = plt.subplots()
tam_g1.plot(ax=ax)
ax.set_xlim(0, 48)
ax.set_ylim(0, 4)
ax.set_title("Citronensäure in CEM I 42.5R", fontsize=11)
plt.show()

#%%

fig, ax = plt.subplots()
tam_g2.plot(ax=ax)
ax.set_xlim(0, 48)
ax.set_ylim(0, 4)
ax.set_title("Citronensäure in CEM I 52.5N", fontsize=11)
plt.show()


# %%
plot_configs = [
    {"ycol": "normalized_heat_flow_w_g", "xlim": 1, "ylim": 0.10,  "title": "Heat flow – first hour"},
    {"ycol": "normalized_heat_flow_w_g", "xlim": 48, "ylim": 0.0035,"title": "Heat flow – 48 h"},
    {"ycol": "normalized_heat_j_g", "xlim": 1, "ylim": 50, "title": "Heat – first hour"},
    {"ycol": "normalized_heat_j_g", "xlim": 48, "ylim": 300, "title": "Heat – 48 h"},
]

fig, axs = plt.subplots(2, 2, layout="constrained")
for ax, config in zip(axs.flatten(), plot_configs):
    tam_g1.plot(y=config["ycol"], t_unit="h", y_unit_milli=False, ax=ax)
    ax.set_xlim(0, config["xlim"])
    ax.set_ylim(0, config["ylim"])
    ax.get_legend().remove()
    ax.set_title(config.get(config["ycol"]))
    ax.set_xlabel(config.get("xlabel", "Time [h]"))
    fig.suptitle("Mein Citronensäure-Experiment", fontsize=11)
plt.show()


# %%
plot_configs = [
    {"ycol": "normalized_heat_flow_w_g", "xlim": 1, "ylim": 0.10,  "title": "Heat flow – first hour"},
    {"ycol": "normalized_heat_flow_w_g", "xlim": 48, "ylim": 0.0035,"title": "Heat flow – 48 h"},
    {"ycol": "normalized_heat_j_g", "xlim": 1, "ylim": 50, "title": "Heat – first hour"},
    {"ycol": "normalized_heat_j_g", "xlim": 48, "ylim": 300, "title": "Heat – 48 h"},
]

fig, axs = plt.subplots(2, 2, layout="constrained")
for ax, config in zip(axs.flatten(), plot_configs):
    tam_g2.plot(y=config["ycol"], t_unit="h", y_unit_milli=False, ax=ax)
    ax.set_xlim(0, config["xlim"])
    ax.set_ylim(0, config["ylim"])
    ax.get_legend().remove()
    ax.set_title(config.get(config["ycol"]))
    ax.set_xlabel(config.get("xlabel", "Time [h]"))
    fig.suptitle("Mein Citronensäure-Experiment", fontsize=11)
plt.show()


# %%


group1_ids = ["122", "260", "259", "258", "257"]
group2_ids = ["345", "347", "348", "349", "350"]

regex_group1 = r"JAA_CAL(" + "|".join(group1_ids) + r")\.csv"
regex_group2 = r"JAA_CAL(" + "|".join(group2_ids) + r")\.csv"

tam_g1 = Measurement(calodatapath, regex=regex_group1)
tam_g2 = Measurement(calodatapath, regex=regex_group2)

plot_configs = [
    {"ycol": "normalized_heat_flow_w_g", "xlim": 1,  "ylim": 0.10,  "title": "Heat flow – first hour"},
    {"ycol": "normalized_heat_flow_w_g", "xlim": 48, "ylim": 0.0035,"title": "Heat flow – 48 h"},
    {"ycol": "normalized_heat_j_g",      "xlim": 1,  "ylim": 50,    "title": "Heat – first hour"},
    {"ycol": "normalized_heat_j_g",      "xlim": 48, "ylim": 300,   "title": "Heat – 48 h"},
]

def plot_group(tam, suptitle):
    fig, axs = plt.subplots(2, 2, layout="constrained")

    for ax, config in zip(axs.flatten(), plot_configs):
        tam.plot(
            y=config["ycol"],
            t_unit="h",
            y_unit_milli=False,
            ax=ax,
        )
        ax.set_xlim(0, config["xlim"])
        ax.set_ylim(0, config["ylim"])
        ax.get_legend().remove()

        # Titel pro Subplot
        ax.set_title(config.get("title", config["ycol"]))
        # x-Achsenbeschriftung
        ax.set_xlabel(config.get("xlabel", "Time [h]"))

    fig.suptitle(suptitle, fontsize=11)
    plt.show()


# Gruppe 1: 122 + 260, 259, 258, 257
plot_group(tam_g1, "CEM I 42,5R mit Citronensäure")

# Gruppe 2: 345 + 347, 348, 349, 350
plot_group(tam_g2, "CEM 52,5N mit Citronensäure")

# %%
