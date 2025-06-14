# -*- coding: utf-8 -*-
"""FP-Growth combined with an attention mechanism.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1urPs5dZQMuUbqemYCuz7pPdMU6WPRdUm
"""

#Dataset
#energydata_complete
#Tetuan City power consumption

from google.colab import drive
drive.mount('/content/drive')

import os
os.chdir(r"/content/drive/My Drive")

from google.colab import files
uploaded = files.upload()

import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.frequent_patterns import association_rules

# Load the dataset
grocery_df = pd.read_csv("grocery_dataset.csv")
grocery_df['Items'] = grocery_df['Items'].apply(eval)  # Convert strings back to lists

# Preprocess the data using one-hot encoding
mlb = MultiLabelBinarizer()
encoded_data = pd.DataFrame(
    mlb.fit_transform(grocery_df['Items']),
    columns=mlb.classes_,
    index=grocery_df.index
)

# Step 1: Apply FP-Growth to generate frequent itemsets
min_support = 0.4  # Set minimum support threshold
frequent_itemsets = fpgrowth(encoded_data, min_support=min_support, use_colnames=True)

# Step 2: Enhance with an Attention Mechanism
# Define an attention score based on frequency and item importance
frequent_itemsets['attention_score'] = frequent_itemsets['support'] * (
    frequent_itemsets['itemsets'].apply(lambda x: sum(len(item) for item in x))
)
frequent_itemsets = frequent_itemsets.sort_values(by='attention_score', ascending=False)

# Step 3: Generate Association Rules
min_confidence = 0.6  # Set minimum confidence threshold
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence, num_itemsets=len(encoded_data))
#rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)

# Step 4: Visualization
# Plot top 10 frequent itemsets by attention score
plt.figure(figsize=(10, 6))
top_itemsets = frequent_itemsets.head(10)
plt.barh(
    [', '.join(list(x)) for x in top_itemsets['itemsets']],
    top_itemsets['attention_score'],
    color='skyblue'
)
plt.xlabel('Attention Score')
plt.ylabel('Itemsets')
plt.title('Top 10 Frequent Itemsets by Attention Score')
plt.gca().invert_yaxis()
plt.show()

# Heatmap of association rules
plt.figure(figsize=(10, 8))
confidence_matrix = pd.crosstab(
    rules['antecedents'].apply(lambda x: ', '.join(list(x))),
    rules['consequents'].apply(lambda x: ', '.join(list(x))),
    values=rules['confidence'],
    aggfunc='mean'
).fillna(0)
sns.heatmap(confidence_matrix, annot=True, cmap='YlGnBu', fmt='.2f')
plt.title('Association Rules Heatmap')
plt.xlabel('Consequents')
plt.ylabel('Antecedents')
plt.show()