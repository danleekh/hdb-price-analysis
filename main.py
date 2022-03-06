import math
import pandas as pd
import numpy as np

def parse_remaining_lease(s):
    # assumes that it is always of the form 'X years Y months' or 'X years'
    # does not validate
    tokens = s.split(' ')
    
    if len(tokens) == 4:
        return int(tokens[0]) * 12 + int(tokens[2])
    elif len(tokens) == 2:
        return int(tokens[0]) * 12
    else:
        raise Error(f'Could not parse remaining lease %s' % format(s))

def derive_columns(df):
    df['remaining_lease_months'] = df['remaining_lease'].apply(parse_remaining_lease)
    df['psm'] = (df['resale_price'] / df['floor_area_sqm']).round(decimals=2)
    df['lease_quantized'] = df['remaining_lease_months'] / 120
    df['lease_quantized'] = df['lease_quantized'].apply(np.floor) * 10

df = pd.read_csv('2017-onwards.csv')
derive_columns(df)

fdf = df[df.flat_type.isin(['4 ROOM','5 ROOM','EXECUTIVE'])]

print('Median transacted price by town, type and lease')
pt = np.round(fdf.pivot_table(index='town', columns=['flat_type', 'lease_quantized'], values='resale_price', aggfunc='median'))
print(pt)

print('Mean transacted price by town, type and lease')
pt = np.round(fdf.pivot_table(index='town', columns=['flat_type', 'lease_quantized'], values='resale_price', aggfunc='mean'))
print(pt)

print('Mean PSM by town, type and lease')
pt = np.round(fdf.pivot_table(index='town', columns=['flat_type', 'lease_quantized'], values='psm', aggfunc='mean'))
print(pt)

print("Potentially bad data")
print(df[df.lease_quantized == 0.0])


