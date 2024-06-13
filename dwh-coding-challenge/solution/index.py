import glob
import os
import pandas as pd
import json

def load_json_files(directory):
    data = []
    for filepath in glob.glob(os.path.join(directory, '*.json')):
        with open(filepath) as f:
            data.append(json.load(f))
    return pd.json_normalize(data, sep='_')

def add_timestamp_column(df, column_name):
    df['timestamp'] = df[column_name]
    return df

def merge_tables_on_timestamps(tables):
    all_timestamps = pd.concat([table['timestamp'] for table in tables]).drop_duplicates().sort_values().reset_index(drop=True)
    all_timestamps = pd.DataFrame(all_timestamps, columns=['timestamp'])

    merged_tables = []
    for table in tables:
        merged_tables.append(all_timestamps.merge(table, on='timestamp', how='left'))

    return merged_tables

def identify_transactions(df):
    # Identify savings account transactions
    savings_transactions = df[['timestamp', 'set_balance']].dropna(subset=['set_balance'])
    savings_transactions['transaction_type'] = 'Savings'
    
    # Identify card transactions
    card_transactions = df[['timestamp', 'set_credit_used']].dropna(subset=['set_credit_used'])
    card_transactions['transaction_type'] = 'Card'
    
    # Combine transactions
    transactions = pd.concat([savings_transactions, card_transactions])
    
    # Sort transactions by timestamp
    transactions = transactions.sort_values(by='timestamp').reset_index(drop=True)
    
    return transactions

def main():
    # Load JSON files from each directory into dataframes
    accounts_df = load_json_files('data/accounts')
    cards_df = load_json_files('data/cards')
    savings_accounts_df = load_json_files('data/savings_accounts')

    # 1. Visualize the complete historical view of each table
    print("Accounts Table:\n", accounts_df.to_string(index=False))
    print("\nCards Table:\n", cards_df.to_string(index=False))
    print("\nSavings Accounts Table:\n", savings_accounts_df.to_string(index=False))

    # Add a timestamp column to each dataframe
    accounts_df = add_timestamp_column(accounts_df, 'ts')
    cards_df = add_timestamp_column(cards_df, 'ts')
    savings_accounts_df = add_timestamp_column(savings_accounts_df, 'ts')

    # Create a set of unique timestamps
    tables = [accounts_df, cards_df, savings_accounts_df]
    merged_tables = merge_tables_on_timestamps(tables)

    # Merge the tables
    denormalized_df = merged_tables[0].merge(merged_tables[1], on='timestamp', suffixes=('_account', '_card'))
    denormalized_df = denormalized_df.merge(merged_tables[2], on='timestamp', suffixes=('', '_savings_account'))

    # Drop unnecessary columns
    columns_to_drop = [col for col in denormalized_df.columns if col.startswith('ts_') or col.startswith('ts')]
    denormalized_df.drop(columns=columns_to_drop, inplace=True)
    
    # 2. Visualize the complete historical table view of the denormalized joined table
    print("\nDenormalized Table:\n", denormalized_df.to_string(index=False))

    # 3. Identify transactions and summarize
    transactions = identify_transactions(denormalized_df)
    transaction_count = len(transactions)
    print(f"\nThere are {transaction_count} transactions:")
    print(transactions.to_string(index=False))

if __name__ == "__main__":
        main()