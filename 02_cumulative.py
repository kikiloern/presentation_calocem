#%%
import os
from calocem import tacalorimetry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
from pathlib import Path
#%%
pathname = os.path.dirname(os.path.realpath(__file__))
path_to_data = pathname + os.sep + "data"
outputpath = Path(pathname) / "output"

tam = tacalorimetry.Measurement(folder=path_to_data,
                                regex=r"JAA_CAL(122|345)\.csv",
                                )

# get sample and information
data = tam.get_data()
info = tam.get_information()

data
# %%

fig, (ax_flow, ax_heat) = plt.subplots(1, 2, figsize=(10, 4), sharex=True)
ax_flow = tam.plot(
    t_unit="h",
    y='normalized_heat_flow_w_g',
    y_unit_milli=False,
    ax=ax_flow,  
)
# show cumulated heat plot
ax_heat = tam.plot(
    t_unit="h",
    y='normalized_heat_j_g',
    y_unit_milli=False,
    ax=ax_heat,  
)

label_map = {
    "JAA_CAL122": "CEM I 42.5R",
    "JAA_CAL345": "CEM I 52.5N",
}

for ax in (ax_flow, ax_heat):
    handles, labels = ax.get_legend_handles_labels()
    new_labels = [label_map.get(lbl, lbl) for lbl in labels]
    ax.legend(handles, new_labels, title="Bindemittel")
# define target time
target_h = 24

# guide to the eye line
ax_heat.axvline(target_h, color="gray", alpha=0.5, linestyle=":")
ax_flow.axvline(target_h, color="gray", alpha=0.5, linestyle=":")
# set upper limits
ax_flow.set_ylim(0,0.005)
ax_flow.set_xlim(0,48)
ax_heat.set_ylim(0,400)
ax_heat.set_xlim(0,48)
ax_heat.set_title("Cumulated Heat")
ax_flow.set_title("Heat Flow")  
ax_flow.set_xlabel("Time [h]")
ax_heat.set_xlabel("Time [h]")
# show plot
tacalorimetry.plt.show()
# %%
# get table of cumulated heat at certain age
cumulated_heats = tam.get_cumulated_heat_at_hours(
          target_h=target_h,
          cutoff_min=15
          )

# show result
print(cumulated_heats)
cumulated_heats
#%%
label_map = {
    "JAA_CAL122": "CEM I 42.5R",
    "JAA_CAL345": "CEM I 52.5N",
}

# DIN A4 quer
A4_LANDSCAPE = (11.69, 8.27)
pdf_path = Path(pathname) / "output"
pdf_path = outputpath / "your_baumit_austria_cem_comparison.pdf"

with PdfPages(pdf_path) as pdf:
    # Figure mit GridSpec: oben 2 Plots, unten Tabelle
    fig = plt.figure(figsize=A4_LANDSCAPE)
    gs = fig.add_gridspec(2, 2, height_ratios=[2, 1])

    # --- LINKS OBEN: Heat Flow ---
    ax_flow = fig.add_subplot(gs[0, 0])
    tam.plot(
        t_unit="h",
        y="normalized_heat_flow_w_g",
        y_unit_milli=False,
        ax=ax_flow,
    )
    ax_flow.set_title("Heat Flow", fontsize=9)
    ax_flow.set_xlabel("Time [h]")
    ax_flow.set_ylabel("Normalized Heat Flow [W/g]")

    # --- RECHTS OBEN: Cumulated Heat ---
    ax_heat = fig.add_subplot(gs[0, 1])
    tam.plot(
        t_unit="h",
        y="normalized_heat_j_g",
        y_unit_milli=False,
        ax=ax_heat,
    )
    ax_heat.set_title("Cumulated Heat", fontsize=9)
    ax_heat.set_xlabel("Time [h]")
    ax_heat.set_ylabel("Normalized Heat [J/g]")


    for ax in (ax_flow, ax_heat):
        handles, labels = ax.get_legend_handles_labels()
        new_labels = [label_map.get(lbl, lbl) for lbl in labels]
        ax.legend(handles, new_labels, title="Bindemittel", fontsize=7, title_fontsize=8)


    ax_heat.axvline(target_h, color="gray", alpha=0.5, linestyle=":")
    ax_flow.axvline(target_h, color="gray", alpha=0.5, linestyle=":")


    ax_flow.set_ylim(0, 0.005)
    ax_flow.set_xlim(0, 48)
    ax_heat.set_ylim(0, 400)
    ax_heat.set_xlim(0, 48)


    ax_table = fig.add_subplot(gs[1, :])
    ax_table.axis("off")


    ch = cumulated_heats.copy()

    if isinstance(ch, pd.Series):
        ch = ch.to_frame(name=f"Q_{target_h}h [J/g]")


    if "sample_short" not in ch.columns:
        ch = ch.reset_index().rename(columns={ch.columns[0]: "sample_short"})

 
    ch["Bindemittel"] = ch["sample_short"].map(label_map)

    # Spalten sortieren: Binder zuerst, dann Rest
    cols = ["Bindemittel"] + [c for c in ch.columns if c not in ["Bindemittel", "sample_short"]]
    ch = ch[cols]

    ch_print = ch.round(2)

    table = ax_table.table(
        cellText=ch_print.values,
        colLabels=ch_print.columns,
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.3)

    ax_table.set_title(
        f"Cumulated Heat at {target_h} h (cutoff ≥ {15} min)",
        fontsize=9,
        pad=8,
    )

    # Gesamttitel
    fig.suptitle("Comparison of CEM I 42.5R vs CEM I 52.5N", fontsize=11, y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    pdf.savefig(fig)
    plt.close(fig)

print(f"PDF written to: {pdf_path}")




# %%
