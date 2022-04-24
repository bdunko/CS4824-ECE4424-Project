from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.datasets import load_iris
from sklearn import preprocessing
import pandas as pd
import numpy as np
import csv

with open('large.csv', 'r') as large_file:
    column_names = next(large_file).replace('\n', '').split(',')
    large_dataset = csv.reader(large_file)
    large_dataset = pd.DataFrame([row for row in large_dataset], columns=column_names)

large_dataset['T1P1WINRATE'] = large_dataset['T1P1WINRATE'].astype(float)
large_dataset['T1P2WINRATE'] = large_dataset['T1P2WINRATE'].astype(float)
large_dataset['T1P3WINRATE'] = large_dataset['T1P3WINRATE'].astype(float)
large_dataset['T1P4WINRATE'] = large_dataset['T1P4WINRATE'].astype(float)
large_dataset['T1P5WINRATE'] = large_dataset['T1P5WINRATE'].astype(float)
large_dataset['T2P1WINRATE'] = large_dataset['T2P1WINRATE'].astype(float)
large_dataset['T2P2WINRATE'] = large_dataset['T2P2WINRATE'].astype(float)
large_dataset['T2P3WINRATE'] = large_dataset['T2P3WINRATE'].astype(float)
large_dataset['T2P4WINRATE'] = large_dataset['T2P4WINRATE'].astype(float)
large_dataset['T2P5WINRATE'] = large_dataset['T2P5WINRATE'].astype(float)

conditions_P1T1 = [
    (large_dataset['T1P1WINRATE'] < 0.4),
    ((large_dataset['T1P1WINRATE'] >= 0.4) & (large_dataset['T1P1WINRATE'] < 0.45)),
    ((large_dataset['T1P1WINRATE'] >= 0.45) & (large_dataset['T1P1WINRATE'] < 0.5)),
    ((large_dataset['T1P1WINRATE'] >= 0.5) & (large_dataset['T1P1WINRATE'] < 0.55)),
    ((large_dataset['T1P1WINRATE'] >= 0.55) & (large_dataset['T1P1WINRATE'] < 0.6)),
    (large_dataset['T1P1WINRATE'] >= 0.6)]

conditions_P2T1 = [
    (large_dataset['T1P2WINRATE'] < 0.4),
    ((large_dataset['T1P2WINRATE'] >= 0.4) & (large_dataset['T1P2WINRATE'] < 0.45)),
    ((large_dataset['T1P2WINRATE'] >= 0.45) & (large_dataset['T1P2WINRATE'] < 0.5)),
    ((large_dataset['T1P2WINRATE'] >= 0.5) & (large_dataset['T1P2WINRATE'] < 0.55)),
    ((large_dataset['T1P2WINRATE'] >= 0.55) & (large_dataset['T1P2WINRATE'] < 0.6)),
    (large_dataset['T1P2WINRATE'] >= 0.6)]

conditions_P3T1 = [
    (large_dataset['T1P3WINRATE'] < 0.4),
    ((large_dataset['T1P3WINRATE'] >= 0.4) & (large_dataset['T1P3WINRATE'] < 0.45)),
    ((large_dataset['T1P3WINRATE'] >= 0.45) & (large_dataset['T1P3WINRATE'] < 0.5)),
    ((large_dataset['T1P3WINRATE'] >= 0.5) & (large_dataset['T1P3WINRATE'] < 0.55)),
    ((large_dataset['T1P3WINRATE'] >= 0.55) & (large_dataset['T1P3WINRATE'] < 0.6)),
    (large_dataset['T1P3WINRATE'] >= 0.6)]

conditions_P4T1 = [
    (large_dataset['T1P4WINRATE'] < 0.4),
    ((large_dataset['T1P4WINRATE'] >= 0.4) & (large_dataset['T1P4WINRATE'] < 0.45)),
    ((large_dataset['T1P4WINRATE'] >= 0.45) & (large_dataset['T1P4WINRATE'] < 0.5)),
    ((large_dataset['T1P4WINRATE'] >= 0.5) & (large_dataset['T1P4WINRATE'] < 0.55)),
    ((large_dataset['T1P4WINRATE'] >= 0.55) & (large_dataset['T1P4WINRATE'] < 0.6)),
    (large_dataset['T1P4WINRATE'] >= 0.6)]

conditions_P5T1 = [
    (large_dataset['T1P5WINRATE'] < 0.4),
    ((large_dataset['T1P5WINRATE'] >= 0.4) & (large_dataset['T1P5WINRATE'] < 0.45)),
    ((large_dataset['T1P5WINRATE'] >= 0.45) & (large_dataset['T1P5WINRATE'] < 0.5)),
    ((large_dataset['T1P5WINRATE'] >= 0.5) & (large_dataset['T1P5WINRATE'] < 0.55)),
    ((large_dataset['T1P5WINRATE'] >= 0.55) & (large_dataset['T1P5WINRATE'] < 0.6)),
    (large_dataset['T1P5WINRATE'] >= 0.6)]

conditions_P1T2 = [
    (large_dataset['T2P1WINRATE'] < 0.4),
    ((large_dataset['T2P1WINRATE'] >= 0.4) & (large_dataset['T2P1WINRATE'] < 0.45)),
    ((large_dataset['T2P1WINRATE'] >= 0.45) & (large_dataset['T2P1WINRATE'] < 0.5)),
    ((large_dataset['T2P1WINRATE'] >= 0.5) & (large_dataset['T2P1WINRATE'] < 0.55)),
    ((large_dataset['T2P1WINRATE'] >= 0.55) & (large_dataset['T2P1WINRATE'] < 0.6)),
    (large_dataset['T2P1WINRATE'] >= 0.6)]

conditions_P2T2 = [
    (large_dataset['T2P2WINRATE'] < 0.4),
    ((large_dataset['T2P2WINRATE'] >= 0.4) & (large_dataset['T2P2WINRATE'] < 0.45)),
    ((large_dataset['T2P2WINRATE'] >= 0.45) & (large_dataset['T2P2WINRATE'] < 0.5)),
    ((large_dataset['T2P2WINRATE'] >= 0.5) & (large_dataset['T2P2WINRATE'] < 0.55)),
    ((large_dataset['T2P2WINRATE'] >= 0.55) & (large_dataset['T2P2WINRATE'] < 0.6)),
    (large_dataset['T2P2WINRATE'] >= 0.6)]

conditions_P3T2 = [
    (large_dataset['T2P3WINRATE'] < 0.4),
    ((large_dataset['T2P3WINRATE'] >= 0.4) & (large_dataset['T2P3WINRATE'] < 0.45)),
    ((large_dataset['T2P3WINRATE'] >= 0.45) & (large_dataset['T2P3WINRATE'] < 0.5)),
    ((large_dataset['T2P3WINRATE'] >= 0.5) & (large_dataset['T2P3WINRATE'] < 0.55)),
    ((large_dataset['T2P3WINRATE'] >= 0.55) & (large_dataset['T2P3WINRATE'] < 0.6)),
    (large_dataset['T2P3WINRATE'] >= 0.6)]

conditions_P4T2 = [
    (large_dataset['T2P4WINRATE'] < 0.4),
    ((large_dataset['T2P4WINRATE'] >= 0.4) & (large_dataset['T2P4WINRATE'] < 0.45)),
    ((large_dataset['T2P4WINRATE'] >= 0.45) & (large_dataset['T2P4WINRATE'] < 0.5)),
    ((large_dataset['T2P4WINRATE'] >= 0.5) & (large_dataset['T2P4WINRATE'] < 0.55)),
    ((large_dataset['T2P4WINRATE'] >= 0.55) & (large_dataset['T2P4WINRATE'] < 0.6)),
    (large_dataset['T2P4WINRATE'] >= 0.6)]

conditions_P5T2 = [
    (large_dataset['T2P5WINRATE'] < 0.4),
    ((large_dataset['T2P5WINRATE'] >= 0.4) & (large_dataset['T2P5WINRATE'] < 0.45)),
    ((large_dataset['T2P5WINRATE'] >= 0.45) & (large_dataset['T2P5WINRATE'] < 0.5)),
    ((large_dataset['T2P5WINRATE'] >= 0.5) & (large_dataset['T2P5WINRATE'] < 0.55)),
    ((large_dataset['T2P5WINRATE'] >= 0.55) & (large_dataset['T2P5WINRATE'] < 0.6)),
    (large_dataset['T2P5WINRATE'] >= 0.6)]

win_loss_classifications = ['Below 40% W/L', '40-45% W/L', '45-50% W/L', '50-55% W/L', '55-60% W/L', 'Above 60% W/L']

large_dataset['T1P1WINRATECLASS'] = np.select(conditions_P1T1, win_loss_classifications, "Error")
large_dataset['T1P2WINRATECLASS'] = np.select(conditions_P2T1, win_loss_classifications, "Error")
large_dataset['T1P3WINRATECLASS'] = np.select(conditions_P3T1, win_loss_classifications, "Error")
large_dataset['T1P4WINRATECLASS'] = np.select(conditions_P4T1, win_loss_classifications, "Error")
large_dataset['T1P5WINRATECLASS'] = np.select(conditions_P5T1, win_loss_classifications, "Error")
large_dataset['T2P1WINRATECLASS'] = np.select(conditions_P1T2, win_loss_classifications, "Error")
large_dataset['T2P2WINRATECLASS'] = np.select(conditions_P2T2, win_loss_classifications, "Error")
large_dataset['T2P3WINRATECLASS'] = np.select(conditions_P3T2, win_loss_classifications, "Error")
large_dataset['T2P4WINRATECLASS'] = np.select(conditions_P4T2, win_loss_classifications, "Error")
large_dataset['T2P5WINRATECLASS'] = np.select(conditions_P5T2, win_loss_classifications, "Error")

# X = large_dataset[['T1P1RANK', 'T1P1CHAMPION', 'T1P1SPELL1', 'T1P1SPELL2', 'T1P1SUMMONERLEVEL', 'T1P1WINRATECLASS',
#                     'T1P2RANK', 'T1P2CHAMPION', 'T1P2SPELL1', 'T1P2SPELL2', 'T1P2SUMMONERLEVEL', 'T1P2WINRATECLASS',
#                     'T1P3RANK', 'T1P3CHAMPION', 'T1P3SPELL1', 'T1P3SPELL2', 'T1P3SUMMONERLEVEL', 'T1P3WINRATECLASS',
#                     'T1P4RANK', 'T1P4CHAMPION', 'T1P4SPELL1', 'T1P4SPELL2', 'T1P4SUMMONERLEVEL', 'T1P4WINRATECLASS',
#                     'T1P5RANK', 'T1P5CHAMPION', 'T1P5SPELL1', 'T1P5SPELL2', 'T1P5SUMMONERLEVEL', 'T1P5WINRATECLASS',
#                     'T2P1RANK', 'T2P1CHAMPION', 'T2P1SPELL1', 'T2P1SPELL2', 'T2P1SUMMONERLEVEL', 'T2P1WINRATECLASS',
#                     'T2P2RANK', 'T2P2CHAMPION', 'T2P2SPELL1', 'T2P2SPELL2', 'T2P2SUMMONERLEVEL', 'T2P2WINRATECLASS',
#                     'T2P3RANK', 'T2P3CHAMPION', 'T2P3SPELL1', 'T2P3SPELL2', 'T2P3SUMMONERLEVEL', 'T2P3WINRATECLASS',
#                     'T2P4RANK', 'T2P4CHAMPION', 'T2P4SPELL1', 'T2P4SPELL2', 'T2P4SUMMONERLEVEL', 'T2P4WINRATECLASS',
#                     'T2P5RANK', 'T2P5CHAMPION', 'T2P5SPELL1', 'T2P5SPELL2', 'T2P5SUMMONERLEVEL', 'T2P5WINRATECLASS']]

X = large_dataset[['T1P1CHAMPION', 'T1P1SPELL1', 'T1P1SPELL2', 'T1P1WINRATECLASS',
                    'T1P2CHAMPION', 'T1P2SPELL1', 'T1P2SPELL2', 'T1P2WINRATECLASS',
                    'T1P3CHAMPION', 'T1P3SPELL1', 'T1P3SPELL2', 'T1P3WINRATECLASS',
                    'T1P4CHAMPION', 'T1P4SPELL1', 'T1P4SPELL2', 'T1P4WINRATECLASS',
                    'T1P5CHAMPION', 'T1P5SPELL1', 'T1P5SPELL2', 'T1P5WINRATECLASS',
                    'T2P1CHAMPION', 'T2P1SPELL1', 'T2P1SPELL2', 'T2P1WINRATECLASS',
                    'T2P2CHAMPION', 'T2P2SPELL1', 'T2P2SPELL2', 'T2P2WINRATECLASS',
                    'T2P3CHAMPION', 'T2P3SPELL1', 'T2P3SPELL2', 'T2P3WINRATECLASS',
                    'T2P4CHAMPION', 'T2P4SPELL1', 'T2P4SPELL2', 'T2P4WINRATECLASS',
                    'T2P5CHAMPION', 'T2P5SPELL1', 'T2P5SPELL2', 'T2P5WINRATECLASS']]

#X_champsT1 = large_dataset.loc[:, 'T1Aatrox':'T1Zyra'].astype(float)
#X_champsT2 = large_dataset.loc[:, 'T2Aatrox':'T2Zyra'].astype(float)

#X[X_champsT1.columns] = X_champsT1
#X[X_champsT2.columns] = X_champsT2

y = large_dataset['WINNINGTEAM']

le = preprocessing.LabelEncoder()
# X['T1P1RANK'] = le.fit_transform(X['T1P1RANK'])
# X['T1P2RANK'] = le.fit_transform(X['T1P2RANK'])
# X['T1P3RANK'] = le.fit_transform(X['T1P3RANK'])
# X['T1P4RANK'] = le.fit_transform(X['T1P4RANK'])
# X['T1P5RANK'] = le.fit_transform(X['T1P5RANK'])
# X['T2P1RANK'] = le.fit_transform(X['T2P1RANK'])
# X['T2P2RANK'] = le.fit_transform(X['T2P2RANK'])
# X['T2P3RANK'] = le.fit_transform(X['T2P3RANK'])
# X['T2P4RANK'] = le.fit_transform(X['T2P4RANK'])
# X['T2P5RANK'] = le.fit_transform(X['T2P5RANK'])

X['T1P1CHAMPION'] = le.fit_transform(X['T1P1CHAMPION'])
X['T1P2CHAMPION'] = le.fit_transform(X['T1P2CHAMPION'])
X['T1P3CHAMPION'] = le.fit_transform(X['T1P3CHAMPION'])
X['T1P4CHAMPION'] = le.fit_transform(X['T1P4CHAMPION'])
X['T1P5CHAMPION'] = le.fit_transform(X['T1P5CHAMPION'])
X['T2P1CHAMPION'] = le.fit_transform(X['T2P1CHAMPION'])
X['T2P2CHAMPION'] = le.fit_transform(X['T2P2CHAMPION'])
X['T2P3CHAMPION'] = le.fit_transform(X['T2P3CHAMPION'])
X['T2P4CHAMPION'] = le.fit_transform(X['T2P4CHAMPION'])
X['T2P5CHAMPION'] = le.fit_transform(X['T2P5CHAMPION'])

X['T1P1SPELL1'] = le.fit_transform(X['T1P1SPELL1'])
X['T1P2SPELL1'] = le.fit_transform(X['T1P2SPELL1'])
X['T1P3SPELL1'] = le.fit_transform(X['T1P3SPELL1'])
X['T1P4SPELL1'] = le.fit_transform(X['T1P4SPELL1'])
X['T1P5SPELL1'] = le.fit_transform(X['T1P5SPELL1'])
X['T2P1SPELL1'] = le.fit_transform(X['T2P1SPELL1'])
X['T2P2SPELL1'] = le.fit_transform(X['T2P2SPELL1'])
X['T2P3SPELL1'] = le.fit_transform(X['T2P3SPELL1'])
X['T2P4SPELL1'] = le.fit_transform(X['T2P4SPELL1'])
X['T2P5SPELL1'] = le.fit_transform(X['T2P5SPELL1'])

X['T1P1SPELL2'] = le.fit_transform(X['T1P1SPELL2'])
X['T1P2SPELL2'] = le.fit_transform(X['T1P2SPELL2'])
X['T1P3SPELL2'] = le.fit_transform(X['T1P3SPELL2'])
X['T1P4SPELL2'] = le.fit_transform(X['T1P4SPELL2'])
X['T1P5SPELL2'] = le.fit_transform(X['T1P5SPELL2'])
X['T2P1SPELL2'] = le.fit_transform(X['T2P1SPELL2'])
X['T2P2SPELL2'] = le.fit_transform(X['T2P2SPELL2'])
X['T2P3SPELL2'] = le.fit_transform(X['T2P3SPELL2'])
X['T2P4SPELL2'] = le.fit_transform(X['T2P4SPELL2'])
X['T2P5SPELL2'] = le.fit_transform(X['T2P5SPELL2'])

# X['T1P1SUMMONERLEVEL'] = le.fit_transform(X['T1P1SUMMONERLEVEL'])
# X['T1P2SUMMONERLEVEL'] = le.fit_transform(X['T1P2SUMMONERLEVEL'])
# X['T1P3SUMMONERLEVEL'] = le.fit_transform(X['T1P3SUMMONERLEVEL'])
# X['T1P4SUMMONERLEVEL'] = le.fit_transform(X['T1P4SUMMONERLEVEL'])
# X['T1P5SUMMONERLEVEL'] = le.fit_transform(X['T1P5SUMMONERLEVEL'])
# X['T2P1SUMMONERLEVEL'] = le.fit_transform(X['T2P1SUMMONERLEVEL'])
# X['T2P2SUMMONERLEVEL'] = le.fit_transform(X['T2P2SUMMONERLEVEL'])
# X['T2P3SUMMONERLEVEL'] = le.fit_transform(X['T2P3SUMMONERLEVEL'])
# X['T2P4SUMMONERLEVEL'] = le.fit_transform(X['T2P4SUMMONERLEVEL'])
# X['T2P5SUMMONERLEVEL'] = le.fit_transform(X['T2P5SUMMONERLEVEL'])

X['T1P1WINRATECLASS'] = le.fit_transform(X['T1P1WINRATECLASS'])
X['T1P2WINRATECLASS'] = le.fit_transform(X['T1P2WINRATECLASS'])
X['T1P3WINRATECLASS'] = le.fit_transform(X['T1P3WINRATECLASS'])
X['T1P4WINRATECLASS'] = le.fit_transform(X['T1P4WINRATECLASS'])
X['T1P5WINRATECLASS'] = le.fit_transform(X['T1P5WINRATECLASS'])
X['T2P1WINRATECLASS'] = le.fit_transform(X['T2P1WINRATECLASS'])
X['T2P2WINRATECLASS'] = le.fit_transform(X['T2P2WINRATECLASS'])
X['T2P3WINRATECLASS'] = le.fit_transform(X['T2P3WINRATECLASS'])
X['T2P4WINRATECLASS'] = le.fit_transform(X['T2P4WINRATECLASS'])
X['T2P5WINRATECLASS'] = le.fit_transform(X['T2P5WINRATECLASS'])

y = le.fit_transform(large_dataset['WINNINGTEAM'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
gnb = GaussianNB()
y_pred = gnb.fit(X_train, y_train).predict(X_test)
print("Number of mislabeled points out of a total %d points : %d" % (X_test.shape[0], (y_test != y_pred).sum()))