import pandas as pd
import pyEX as p
import os
import argparse


def main():
    parser = argparse.ArgumentParser('Builds a dataset from a list of ticker symbols.')
    parser.add_argument('--output_folder', type=str)
    parser.add_argument('--ticker_file', type=str)
    parser.add_argument('--api_token', type=str)
    parser.add_argument('--iex_version', type=str)

    args = parser.parse_args()

    tickers = pd.read_csv(args.ticker_file, sep=';')

    pyex_client = p.Client(api_token=args.api_token, version=args.iex_version)

    for i, row in enumerate(tickers.itertuples()):
        path_dict = generate_file_paths(args.output_folder, row.symbol)
        if not check_if_data_exists(path_dict):
            income, balance, cash_flow, charts = get_iex_data(pyex_client, row.symbol)
            write_data_to_disk(income, balance, cash_flow, charts, path_dict)
            

def generate_file_paths(output_base_folder, symbol):

    path_dict = {'output_symbol_folder': os.path.join(output_base_folder, symbol)}

    path_dict['income_file_path'] = os.path.join(path_dict['output_symbol_folder'], 'income.csv')
    path_dict['balance_file_path'] = os.path.join(path_dict['output_symbol_folder'], 'balance.csv')
    path_dict['cash_flow_file_path'] = os.path.join(path_dict['output_symbol_folder'], 'cash_flow.csv')
    path_dict['charts_file_path'] = os.path.join(path_dict['output_symbol_folder'], 'charts.csv')

    return path_dict


def check_if_data_exists(path_dict):
    all_data_exists = False

    if os.path.exists(path_dict['income_file_path']) and os.path.exists(path_dict['balance_file_path']) and \
            os.path.exists(path_dict['cash_flow_file_path']) and os.path.exists(path_dict['charts_file_path']):
        all_data_exists = True

    return all_data_exists


def get_iex_data(client, symbol):
    income = client.incomeStatementDF(symbol, period='quarter', last=12)
    balance = client.balanceSheetDF(symbol, period='quarter', last=12)
    cash_flow = client.cashFlowDF(symbol, period='quarter', last=12)
    charts = client.chartDF(symbol, changeFromClose=True, closeOnly=True, timeframe='5y')

    income = pd.DataFrame(income)
    balance = pd.DataFrame(balance)
    cash_flow = pd.DataFrame(cash_flow)
    charts = pd.DataFrame(charts)

    return income, balance, cash_flow, charts


def write_data_to_disk(income, balance, cash_flow, charts, path_dict):

    if not os.path.exists(path_dict['output_symbol_folder']):
        os.makedirs(path_dict['output_symbol_folder'])

    income.to_csv(path_dict['income_file_path'], sep=';')
    balance.to_csv(path_dict['balance_file_path'], sep=';')
    cash_flow.to_csv(path_dict['cash_flow_file_path'], sep=';')
    charts.to_csv(path_dict['charts_file_path'], sep=';')


if __name__ == "__main__":
    main()


