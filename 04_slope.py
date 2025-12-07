#%%
from pathlib import Path
import calocem.tacalorimetry as ta
from calocem.tacalorimetry import Measurement
from calocem.processparams import ProcessingParameters
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

calodatapath = Path(__file__).parent.parent / 'presentation_calocem' /'data'
outputpath = Path(__file__).parent.parent / 'presentation_calocem' /'output'

# %%
tam = Measurement(calodatapath, regex="JAA_CAL(122|260)")

# %%
fig, ax = plt.subplots()
tam.plot(ax=ax)
ax.set_xlim(0, 48)
ax.set_ylim(0, 4.5)
ax.set_title("Slope Detection")
ax.set_xlabel("Time (h)")
ax.set_ylabel("Normalized heat flow (mW/g)")
plt.show()
# %%
processparams = ProcessingParameters()
processparams.spline_interpolation.apply = True
processparams.spline_interpolation.smoothing_1st_deriv = 1e-12

# get peak onsets via alternative method
fig, ax = ta.plt.subplots()
slope = tam.get_maximum_slope(
    processparams=processparams,
    show_plot=True,
    ax = ax
)
slope
# %%

# Select only the columns you want
slope_data = slope[["sample_short", "td", "gradient"]].copy()

scale_factor = 1e8
slope_data["gradient_x1e8"] = slope_data["gradient"] * scale_factor
slope_data = slope_data.drop(columns=["gradient"])
slope_data = slope_data.rename(
    columns={"gradient_x1e8": "gradient × 1e8"}
)
# Optional: reset index if you don't want the td-index in the file
slope_data = slope_data.reset_index(drop=True)

# Save to Excel (assuming you have outputpath already)
slope_data.to_excel(outputpath / "slopes.xlsx", index=False)
slope_data.to_csv(outputpath / "slopes.csv", index=False)



# %% PDF export: slope plot + table on one DIN A4 page
A4_LANDSCAPE = (11.69, 8.27)
pdf_path = outputpath / "Slope Detection – retardation.pdf"

with PdfPages(pdf_path) as pdf:
    # New figure for the PDF
    fig = plt.figure(figsize=A4_LANDSCAPE)
    gs = fig.add_gridspec(2, 1, height_ratios=[2, 1])

    # --- TOP: slope plot ---
    ax_slope = fig.add_subplot(gs[0, 0])
    # re-plot slopes into this axes
    tam.get_maximum_slope(
        processparams=processparams,
        show_plot=True,
        ax=ax_slope
    )
    ax_slope.set_title("Maximum Slope Detection", fontsize=10)
    ax_slope.set_xlabel("Time (h)")     # falls die Lib das nicht setzt
    ax_slope.set_ylabel("Normalized Heat Flow (W/g)")  # ggf. anpassen

    # --- BOTTOM: table with slope_data ---
    ax_table = fig.add_subplot(gs[1, 0])
    ax_table.axis("off")

    table_df = slope_data.copy().round(4)

    table = ax_table.table(
        cellText=table_df.values,
        colLabels=table_df.columns,
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.2)

    ax_table.set_title(
        "Maximum Slope Data (gradient × 1e8)",
        fontsize=10,
        pad=8,
    )

    fig.suptitle("Slope Detection – retardation", fontsize=12, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    pdf.savefig(fig)
    plt.close(fig)

print(f"PDF written to: {pdf_path}")



# %%
