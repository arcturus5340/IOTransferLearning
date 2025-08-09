#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable


# In[2]:


df = pd.read_csv(Path(r"./captum/Blue_waters_captum_ig_result.csv"))
df_dl = pd.read_csv(Path(r"./captum/Blue_waters_captum_dl_result.csv"))
df_data = pd.read_csv(Path(r"./captum/Blue_waters_captum_test_data.csv"))


# In[3]:


df.head()


# In[4]:


df_dl.head()


# In[5]:


df_diff = df_dl - df
df_diff.describe().transpose()  #.abs().sort_values(ascending=False).head(20)


# **Attention: std sensitive to outliers?**

# In[6]:


plt.rcParams.update({'font.size': 17})
fig, axs = plt.subplots(nrows = 1, ncols=2, figsize=(20,8))
stats_ig = axs[0].scatter(x=df_data['POSIX_STATS'], y=df['POSIX_STATS'])
stats_dl = axs[0].scatter(x=df_data['POSIX_STATS'], y=df_dl['POSIX_STATS'])
axs[0].legend((stats_ig,stats_dl), ("Integrated Gradients", "DeepLIFT"), prop={'size': 16})
axs[0].set_xlabel("POSIX_STATS")
axs[0].set_ylabel("attribution value")
bytes_ig = axs[1].scatter(x=df_data['POSIX_BYTES_WRITTEN'], y=df['POSIX_BYTES_WRITTEN'], label="Integrated Gradients")
bytes_dl = axs[1].scatter(x=df_data['POSIX_BYTES_WRITTEN'], y=df_dl['POSIX_BYTES_WRITTEN'], label="DeepLIFT")
axs[1].legend((bytes_ig,bytes_dl), ("Integrated Gradients", "DeepLIFT"), prop={'size': 16})
axs[1].set_xlabel("POSIX_BYTES_WRITTEN")
axs[1].set_ylabel("attribution value")
plt.savefig("../results/interpretability/Blue_Waters_captum_difference_plot.png", format="png", bbox_inches="tight", dpi=600)


# In[7]:


df_diff["POSIX_OPENS"].sort_values(ascending=False).head()


# In[8]:


df_data.iloc[29918]


# In[9]:


df.iloc[29918].POSIX_OPENS


# In[10]:


df_dl.iloc[29918].POSIX_OPENS


# In[11]:


df.describe().transpose()


# Compute distance to baseline per row. Baseline output is about 75, so be careful with the interpretation around ig_value of 0!

# In[12]:


df.sum(axis=1).describe()


# In[13]:


df_dl.sum(axis=1).describe()


# In[14]:


df_data.nprocs


# In[15]:


df_data.index


# In[16]:


df_data.head()


# In[17]:


len(df_data)


# In[18]:


df_data.nprocs.unique()


# - nprocs: only important if it gets really high.
# - CONSEC_READS: if reads are consecutive, performance is better.
# - CONSEC_WRITES: if writes are consecutive, performance is worse. Why??
# - rank: in 56% of the entire dataset the rank is -1, so probably unknown

# In[19]:


plt.rcParams.update({'font.size': 23})


# In[20]:


def plot_df_w_filter(df,filterexp,column,coord,color_column="POSIX_BYTES_READ"):
    df[filterexp].plot.scatter(x=df.column,y=df_data.column, ax=coord,
                                                 c=np.log10(df_no_outliers[filterexp].POSIX_BYTES_READ),colorbar=True)


# In[21]:


def plot_mosaic(filter_spec):
    fig, axs = plt.subplots(nrows = 3, ncols=3, figsize=(30, 20))
    plot_df_w_filter(df_no_outliers,filter_spec,"nprocs",axs[0,0])
    plot_df_w_filter(df_no_outliers,filter_spec,"POSIX_READS",axs[0,1])
    plot_df_w_filter(df_no_outliers,filter_spec,"POSIX_CONSEC_READS",axs[0,2])
    plot_df_w_filter(df_no_outliers,filter_spec,"POSIX_WRITES",axs[1,0],"POSIX_BYTES_WRITTEN")
    df_no_outliers[filter_spec].plot.scatter(x="POSIX_BYTES_READ",y="POSIX_TOTAL_TIME",ax=axs[1,1])
    plt.show()


# In[22]:


bytes_read_copy = df_data.POSIX_BYTES_READ.copy().where(df_data.POSIX_BYTES_READ > 0,0.1)
bytes_written_copy = df_data.POSIX_BYTES_WRITTEN.copy().where(df_data.POSIX_BYTES_WRITTEN > 0,0.1)
fig, axs = plt.subplots(nrows = 2, ncols=3, figsize=(30, 20))
[ax.set_ylabel("ig_value") for axs_x in axs for ax in axs_x]
reads_filter = df_data.POSIX_READS < 0.5e8
sc_read = axs[0,0].scatter(x=df_data[reads_filter].POSIX_READS,y=df[reads_filter].POSIX_READS,c=np.log10(bytes_read_copy[reads_filter]))
axs[0,0].set_xlabel("POSIX_READS")
nprocs_filter = df_data.nprocs < 5000
axs[0,1].scatter(x=df_data[nprocs_filter].nprocs,y=df[nprocs_filter].nprocs,c=np.log10(bytes_read_copy[nprocs_filter]))
axs[0,1].set_xlabel("nprocs")
consec_reads_filter = df_data.POSIX_CONSEC_READS < 0.5e8
axs[0,2].scatter(x=df_data[consec_reads_filter].POSIX_CONSEC_READS,y=df[consec_reads_filter].POSIX_CONSEC_READS,c=np.log10(bytes_read_copy[consec_reads_filter]))
axs[0,2].set_xlabel("POSIX_CONSEC_READS")
sc_written = axs[1,0].scatter(x=df_data.POSIX_CONSEC_WRITES,y=df.POSIX_CONSEC_WRITES,c=np.log10(bytes_written_copy),cmap="plasma")
axs[1,0].set_xlabel("POSIX_CONSEC_WRITES")
axs[1,1].scatter(x=df_data.POSIX_MMAPS,y=df.POSIX_MMAPS,c=np.log10(bytes_read_copy))
axs[1,1].set_xlabel("POSIX_MMAPS")
rank_filter = df_data["rank"] == -1
axs[1,2].scatter(x=df_data["rank"][rank_filter == False],y=df["rank"][rank_filter == False],c=np.log10(bytes_read_copy[rank_filter == False]))
axs[1,2].set_xlabel("rank")

fig.subplots_adjust(right=0.92)
cbar_ax_read = fig.add_axes([0.93, 0.15, 0.015, 0.7])
cbar_ax_write = fig.add_axes([0.97, 0.15, 0.015, 0.7])
fig.colorbar(sc_read,cax=cbar_ax_read, shrink=0.7,label="POSIX_BYTES_READ")
fig.colorbar(sc_written,cax=cbar_ax_write, shrink=0.7,label="POSIX_BYTES_WRITTEN")


# In[23]:


plt.rcParams.update({'font.size': 17})
bytes_read_copy = df_data.POSIX_BYTES_READ.copy().where(df_data.POSIX_BYTES_READ > 0,0.1)
bytes_written_copy = df_data.POSIX_BYTES_WRITTEN.copy().where(df_data.POSIX_BYTES_WRITTEN > 0,0.1)
fig, axs = plt.subplots(nrows = 3, ncols=1, figsize=(10, 30))
[ax.set_ylabel("attribution value") for ax in axs]
reads_filter = df_data.POSIX_READS < 0.5e8
sc_read = axs[0].scatter(x=df_data[reads_filter].POSIX_READS,y=df[reads_filter].POSIX_READS,c=np.log10(bytes_read_copy[reads_filter]))
axs[0].set_xlabel("POSIX_READS")
consec_reads_filter = df_data.POSIX_CONSEC_READS < 0.5e8
sc_consec_read = axs[1].scatter(x=df_data[consec_reads_filter].POSIX_CONSEC_READS,y=df[consec_reads_filter].POSIX_CONSEC_READS,c=np.log10(bytes_read_copy[consec_reads_filter]))
axs[1].set_xlabel("POSIX_CONSEC_READS")
nprocs_filter = df_data.nprocs < 5000
sc_nprocs = axs[2].scatter(x=df_data[nprocs_filter].nprocs,y=df[nprocs_filter].nprocs)
axs[2].set_xlabel("nprocs")

divider = make_axes_locatable(axs[0])
cax = divider.append_axes('right', size='5%', pad=0.05)
fig.colorbar(sc_read, cax=cax, orientation='vertical',label="POSIX_BYTES_READ")
divider = make_axes_locatable(axs[1])
cax = divider.append_axes('right', size='5%', pad=0.05)
fig.colorbar(sc_consec_read, cax=cax, orientation='vertical',label="POSIX_BYTES_READ")
plt.savefig("../results/interpretability/Blue_Water_captum_plot_IQR_small.png",format="png",bbox_inches="tight",dpi=600)


# In[24]:


plt.rcParams.update({'font.size': 23})
bytes_read_copy = df_data.POSIX_BYTES_READ.copy().where(df_data.POSIX_BYTES_READ > 0,0.1)
bytes_written_copy = df_data.POSIX_BYTES_WRITTEN.copy().where(df_data.POSIX_BYTES_WRITTEN > 0,0.1)
fig, axs = plt.subplots(nrows = 1, ncols=2, figsize=(30, 10))
plt.subplots_adjust(wspace=0.26)
[ax.set_ylabel("attribution value") for ax in axs]
reads_filter = df_data.POSIX_READS < 0.5e8
sc_read = axs[0].scatter(x=df_data[reads_filter].POSIX_READS,y=df[reads_filter].POSIX_READS,c=np.log10(bytes_read_copy[reads_filter]))
axs[0].set_xlabel("POSIX_READS")
consec_reads_filter = df_data.POSIX_CONSEC_READS < 0.5e8
sc_consec_read = axs[1].scatter(x=df_data[consec_reads_filter].POSIX_CONSEC_READS,y=df[consec_reads_filter].POSIX_CONSEC_READS,c=np.log10(bytes_read_copy[consec_reads_filter]))
axs[1].set_xlabel("POSIX_CONSEC_READS")
divider = make_axes_locatable(axs[0])
cax = divider.append_axes('right', size='5%', pad=0.05)
fig.colorbar(sc_read, cax=cax, orientation='vertical',label="POSIX_BYTES_READ")
divider = make_axes_locatable(axs[1])
cax = divider.append_axes('right', size='5%', pad=0.05)
fig.colorbar(sc_consec_read, cax=cax, orientation='vertical',label="POSIX_BYTES_READ")
plt.savefig("../results/interpretability/Blue_Water_captum_plot_IQR_small_horizontal.png",format="png",bbox_inches="tight",dpi=600)


# In[25]:


plt.rcParams.update({'font.size': 23})
fig, axs = plt.subplots(nrows = 1, ncols=1, figsize=(10, 10))
plt.subplots_adjust(wspace=0.26)
axs.set_ylabel("attribution value")
nprocs_filter = df_data.nprocs < 5000
sc_nprocs = axs.scatter(x=df_data[nprocs_filter].nprocs,y=df[nprocs_filter].nprocs)
axs.set_xlabel("nprocs")
plt.savefig("../results/interpretability/Blue_Water_captum_plot_IQR_nprocs.png",format="png",bbox_inches="tight",dpi=600)


# ### Compare to the plot for POSIX_CONSEC_READS above. Histogram does not tell anything!

# In[26]:


df.POSIX_CONSEC_READS.hist(bins=50)


# In[ ]:




