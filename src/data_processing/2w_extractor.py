import pandas
import numpy as np
import argparse
from re import sub

parser = argparse.ArgumentParser(description='Extracts features from raw data and outputs them into a csv file')

parser.add_argument('--input', metavar='i', type=str, help='Path and name to the raw data (csv format). Example: "/data/raw/msft.csv"')
parser.add_argument('--output', metavar='o', type=str, help='Path to the new files. Output from extractor will be generated as 2w_input.npy and 2w_labels.npy in that stock tickers folder. Example: "/data/processed" with stock ticker "MSFT" will produce "/data/processed/MSFT/2w_input.npy" and "/data/processed/MSFT/2w_labels.npy"')
parser.add_argument('--ticker', metavar='t', type=str, help='Stock ticker. Example: "MSFT"')

args = parser.parse_args()

raw_data = pandas.read_csv(args.input)

input_data = []
input_filename = args.output + '/' + args.ticker + '/2w_input'
labels = []
labels_filename = args.output + '/' + args.ticker + '/2w_labels'

def convert_currency_to_float(currency):
    float_n = float(sub(r'[^\d.]', '', currency))
    return float_n

for index, row in raw_data.iterrows():
    # Using close price as label
    labels.append(convert_currency_to_float(row['Close']))
    if (index +15 < len(raw_data)):
        # Input data is the data from the preceedign two weeks.
        input_slice = raw_data[index+1:index+15].copy()
        input = []
        for s_index, s_row in input_slice.iterrows():
            s_close = convert_currency_to_float(s_row['Close'])
            s_volume = s_row['Volume']
            s_open = convert_currency_to_float(s_row['Open'])
            s_high = convert_currency_to_float(s_row['High'])
            s_low = convert_currency_to_float(s_row['Low'])
            input.append([s_close, s_volume, s_open, s_high, s_low])
        input_data.append(input)

np_input_data = np.asarray(input_data)
np_labels = np.asarray(labels)

np.save(input_filename, np_input_data)
np.save(labels_filename, np_labels)
