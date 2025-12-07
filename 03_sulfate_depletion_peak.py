#%%
from pathlib import Path
from calocem import tacalorimetry as ta
from calocem.processparams import ProcessingParameters

#%%
calodatapath = Path(__file__).parent.parent / 'presentation_calocem' /'data'



# %%
tam = ta.Measurement(
    folder=calodatapath,
    regex=r"JAA_CAL(122|345)\.csv",
    show_info=True,
    auto_clean=False,
    cold_start=True,
)
# %%
processparams = ProcessingParameters()




# Sulfate depletion peak detection


processparams.peakdetection.prominence = 1e-7 #mit sulfate depletion
#processparams.peakdetection.prominence = 1e-4






fig, ax = ta.plt.subplots()

peaks_found = tam.get_peaks(processparams, plt_right_s=3e5, ax=ax, show_plot=True)

ax.set_xlim(0, 100000)
ax.set_ylim(0, 0.005)
ta.plt.show()


# %%
