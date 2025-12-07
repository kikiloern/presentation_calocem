#%%
from pathlib import Path
import calocem.tacalorimetry as ta
from calocem.processparams import ProcessingParameters
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib as mpl

calodatapath = Path(__file__).parent.parent / 'presentation_calocem' /'data'
outputpath = Path(__file__).parent.parent / 'presentation_calocem' /'output'

# 122 Bernburg Referenz
# 345 Karlstadt Referenz

#%%
tam = ta.Measurement(
    folder=calodatapath,
    #regex=r"JAA_CAL.*.csv",
    #regex=r"JAA_CAL345.csv",
    regex=r"JAA_CAL(345|350|349|348|347)\.csv",
    #regex=r"JAA_CAL(122|257|258|259|260)\.csv",
    #regex=pattern,
    show_info=True,
    #auto_clean=True,
    cold_start=True,
)
# %%
# define the processing parameters
processparams = ProcessingParameters()
processparams.peakdetection.prominence = 1e-4

# plot the peak position
fig, ax = ta.plt.subplots()

# get peaks (returns both a dataframe and extends the axes object)
peaks_found = tam.get_peaks(processparams, plt_right_s=3e5, ax=ax, show_plot=True)
ax.set_xlim(0, 200000)
ax.set_ylim(0, 0.004)
ta.plt.show()
peaks_found


# %%

df = peaks_found[0].iloc[:,[0,3,4,5,6,8]].copy()
df.insert(1, "time_h", df["time_s"] / 3600)
df.to_csv(outputpath / "example_get_peaks.csv", index=False)
df.to_excel(outputpath / "example_get_peaks.xlsx", index=False)


#%%
A4_LANDSCAPE = (11.69, 8.27)

#Processing Parameters wie gehabt
processparams = ProcessingParameters()
processparams.peakdetection.prominence = 1e-4

#PDF
pdf_path = outputpath / "your_baumit_austria_data.pdf"

with PdfPages(pdf_path) as pdf:
    fig = ta.plt.figure(figsize=A4_LANDSCAPE)
    gs = fig.add_gridspec(2, 2, height_ratios=[2, 1])  
    max_time_s = 200000
    max_time_h = max_time_s / 3600  # ≈ 55.56 h
    ax_curves = fig.add_subplot(gs[0, 0])
    tam.plot(
        y="normalized_heat_flow_w_g",
        t_unit="h",
        y_unit_milli=False,
        ax=ax_curves,
    )
    ax_curves.set_title("Calorimetry-Kurven ohne Marker", fontsize=9)
    ax_curves.set_xlabel("Time [h]")
    ax_curves.set_ylabel("Normalized Heat Flow [W/g]")
    ax_curves.set_xlim(0, max_time_h)

    ax_peaks = fig.add_subplot(gs[0, 1])
    peaks_found = tam.get_peaks(
        processparams,
        plt_right_s=3e5,
        ax=ax_peaks,
        show_plot=True,      
    )
    ax_peaks.set_xlim(0, 200000)
    ax_peaks.set_ylim(0, 0.004)
    ax_peaks.set_title("Calorimetry-Kurven mit Peak-Markern", fontsize=9)
    ax_peaks.set_xlabel("Time [s]")
    ax_peaks.set_ylabel("Normalized Heat Flow [W/g]")

    ymin, ymax = ax_peaks.get_ylim()
    ax_curves.set_ylim(ymin, ymax)

    df = peaks_found[0].iloc[:, [0, 3, 4, 5, 6, 8]].copy()
    df.insert(1, "time_h", df["time_s"] / 3600)

    df.to_csv(outputpath / "example_get_peaks.csv", index=False)
    df.to_excel(outputpath / "example_get_peaks.xlsx", index=False)

    ax_table = fig.add_subplot(gs[1, :])
    ax_table.axis("off")

    df_for_print = df.round(4)

    table = ax_table.table(
        cellText=df_for_print.values,
        colLabels=df_for_print.columns,
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(7)
    table.scale(1, 1.2)

    ax_table.set_title("Peak-Tabelle (Baumit Austria Daten)", fontsize=9, pad=8)

    fig.suptitle("Your Baumit Austria Data – Calorimetry & Peaks", fontsize=11, y=0.98)

    ta.plt.tight_layout(rect=[0, 0, 1, 0.96])

    pdf.savefig(fig)
    ta.plt.close(fig)

print(f"PDF gespeichert unter: {pdf_path}")
# %%
