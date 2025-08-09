#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import pandas as pd
import numpy as np
from pathlib import Path

import torch.nn as nn
import torch
from captum.attr import IntegratedGradients, DeepLift
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils import resample
import time

import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader, random_split

import matplotlib.pyplot as plt

import pdb
import os
import csv
import pickle

class ConfigStruct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


# In[2]:


config = dict(
    batch_size=2048,
    dropout=0.05,
    random_seed=1234,
)


# In[3]:


config = ConfigStruct(**config)


# In[4]:


device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
print(f"Using {device} device")


# In[5]:


PICKLE_DIR = r"../models/pickle"
ROBUSTSCALER_NAME = r"Model_D_robustscaler"
ROBUSTSCALER_PATH = Path(PICKLE_DIR, ROBUSTSCALER_NAME).with_suffix(".pkl")

INTERPRETABILITY_DIR = r"../interpretability/captum"

MODEL_DIR = r"../models/"
MODEL_FILENAME = "Model_D.tar"
MODEL_PATH = Path(MODEL_DIR, MODEL_FILENAME)


# In[6]:


# Fix seeds for reproducibility
random.seed(config.random_seed)
np.random.seed(config.random_seed)

torch.manual_seed(config.random_seed)
torch.cuda.manual_seed_all(config.random_seed)

torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False


# In[7]:


model = nn.Sequential(
    nn.Linear(89, 512),
    nn.Dropout(p=config.dropout),
    nn.ReLU(),
    nn.Linear(512, 256),
    nn.Dropout(p=config.dropout),
    nn.ReLU(),
    nn.Linear(256, 128),
    nn.Dropout(p=config.dropout),
    nn.ReLU(),
    nn.Linear(128, 1)
).to(device)


# In[8]:


# Load previously trained state if available
if Path(MODEL_PATH).is_file():
    print("Loading pretrained model...")

    checkpoint = torch.load(MODEL_PATH, map_location=torch.device(device))
    model.load_state_dict(checkpoint['model_state_dict'])
    model_epoch = checkpoint['epoch']
    print(f"Current epoch: {model_epoch}")

model.eval()


# In[9]:


X_test = pd.read_csv(Path(INTERPRETABILITY_DIR, r"Model_D_captum_test_data.csv"))
X_test = X_test.drop(['Unnamed: 0', 'index'], axis=1)
X_test.head()


# In[10]:


y_test = X_test.pop('POSIX_TOTAL_TIME')
y_test.head()


# In[11]:


with open(Path(ROBUSTSCALER_PATH), 'rb') as f:
    scaler = pickle.load(f)
scale_factors = scaler.scale_


# In[12]:


X_test_scaled = scaler.transform(X_test)


# In[13]:


tensor_X_test = torch.Tensor(X_test_scaled).to(device)
tensor_y_test = torch.Tensor(y_test.values).view(-1, 1).to(device)


# In[14]:


test_dataset = TensorDataset(tensor_X_test, tensor_y_test)
test_dataloader = DataLoader(test_dataset, batch_size=config.batch_size)


# In[15]:


df_ig_attr_annotated_full = pd.DataFrame([])
df_dl_attr_annotated_full = pd.DataFrame([])


# In[16]:


ig = IntegratedGradients(model)
deep_lift = DeepLift(model)


# In[17]:


test_data = X_test
test_data = test_data.reset_index()
test_data.to_csv("./captum/Blue_waters_captum_test_data.csv")


# In[18]:


# X_test_original = scaler.inverse_transform(X_test)
# df_X_test_original = pd.DataFrame(X_test_original, columns=X_test.columns)
# df_X_test_original.reset_index(drop=True).to_csv("./captum/Blue_waters_captum_test_data.csv", index=False)


# In[19]:


lower = 0
stride = 30000
upper = stride

while lower < len(X_test):
    print(f"lower {lower} to upper {upper}")
    ex = torch.reshape(tensor_X_test[lower:upper], (upper-lower,89))

    print("Integrated Gradients")
    
    ig_attr = ig.attribute(ex, n_steps=50)
    df_ig_attr_annotated_curr = pd.DataFrame(ig_attr.cpu().detach().numpy(), columns = list(X_test.columns))
    df_ig_attr_annotated_full = pd.concat([df_ig_attr_annotated_full,df_ig_attr_annotated_curr])

    print("Deep Lift")
    deep_lift_attr = deep_lift.attribute(ex)
    df_dl_attr_annotated_curr = pd.DataFrame(deep_lift_attr.cpu().detach().numpy(), columns = list(X_test.columns))
    df_dl_attr_annotated_full = pd.concat([df_dl_attr_annotated_full,df_dl_attr_annotated_curr])
    
    lower += stride
    # upper += min(stride,len(X_test) - upper)
    upper = min(lower + stride, len(X_test))


# In[20]:


# df_ig_attr_annotated_full = df_ig_attr_annotated_full * scale_factors
# df_dl_attr_annotated_full = df_dl_attr_annotated_full * scale_factors


# In[21]:


df_ig_attr_annotated_full.reset_index().drop(["index"],axis=1).to_csv("./captum/Blue_waters_captum_ig_result.csv")
df_dl_attr_annotated_full.reset_index().drop(["index"],axis=1).to_csv("./captum/Blue_waters_captum_dl_result.csv")


# In[ ]:





# In[ ]:




