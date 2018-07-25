import numpy as np
import pandas as pd

np.random.seed(1)
full_labels = pd.read_csv('data/food256_label.csv')
full_labels.head()
grouped = full_labels.groupby('filename')
grouped.apply(lambda x: len(x)).value_counts()
gb = full_labels.groupby('filename')
grouped_list = [gb.get_group(x) for x in gb.groups]
print('length of group is: ' + str(len(grouped_list)))
train_index = np.random.choice(len(grouped_list), size=25395, replace=False)
test_index = np.setdiff1d(list(range(31395)), train_index)
print('length of training/test data: '+ str(len(train_index)) + ', ' + str(len(test_index)))
print('Strating producing csv with coreesponding index...')

# take first 31395 files
train = pd.concat([grouped_list[i] for i in train_index])
test = pd.concat([grouped_list[i] for i in test_index])

print('len train/test: ' + str(len(train)) +', ' + str(len(test)))
train.to_csv('data/train_labels.csv', index=None)
test.to_csv('data/test_labels.csv', index=None)
print('Done of spliting.')
print('_______________________________')
