import pandas as pd
from regbot import signal, Regbot

df = pd.read_csv('../jupyter/regpredict_18_train.csv')

y_pred = []
def getSignal(open,close,utcdatetime,dir):
    return signal(open,close,utcdatetime,dir)



df1 = df.tail(600)



# Run all predictions
df1['enter_short_pred'] = df1.apply(lambda row: getSignal(row['open'], row['close'], row['date'],'short'), axis=1)
df1['enter_long_pred'] = df1.apply(lambda row: getSignal(row['open'], row['close'], row['date'],'long'), axis=1)


print(len(df1[df1['enter_short_pred'] == df1['enter_long']]), len(df) )
print(len(df1[df1['enter_long_pred'] == df1['enter_long']]), len(df) )

print(df1[df1['enter_long']==1].head(15))
print(df1[df1['enter_long']==0].head(15))