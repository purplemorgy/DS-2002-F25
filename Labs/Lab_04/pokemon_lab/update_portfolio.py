#!/usr/bin/python3
import json
import os
import pandas as pd
import sys

def _load_lookup_data(lookup_dir):
    all_lookup_df = []
    for file in os.listdir(lookup_dir):
        if file.endswith('.json'):
            filepath = os.path.join(lookup_dir, file)
            with open(filepath, 'r') as f:
                data = json.load(f)

            df = pd.json_normalize(data['data'])

            df['card_market_value'] = df.get('tcgplayer.prices.holofoil.market', pd.Series(0.0))
            df['card_market_value'] = df['card_market_value'].fillna(df.get('tcgplayer.prices.normal.market', 0.0))
            df['card_market_value'] = df['card_market_value'].fillna(0.0)

            df = df.rename(columns={'id': 'card_id', 'name': 'card_name', 'number': 'card_number', 'set.id': 'set_id', 'set.name': 'set_name'})

            all_lookup_df.append(df[['card_id', 'card_name', 'card_number', 'set_id', 'set_name', "card_market_value"]])
    lookup_df = pd.concat(all_lookup_df)
    lookup_df = lookup_df.sort_values(by='card_market_value')
    lookup_df = lookup_df.drop_duplicates(subset=['card_id'], keep='first')
    return lookup_df

def _load_inventory_data(inventory_dir):
    inventory_data = []
    for file in os.listdir(inventory_dir):
        if file.endswith('.csv'):
            filepath = inventory_dir + '/' + file
            inventory_data.append(pd.read_csv(filepath))
        if not inventory_data:
            return pd.DataFrame()
    inventory_df = pd.concat(inventory_data)
    inventory_df['card_id'] = inventory_df['set_id'].astype(str) + '-' + inventory_df['card_number'].astype(str)
    return inventory_df

def update_portfolio(inventory_dir, lookup_dir, output_file):
    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)
    if inventory_df.empty:
        print('Error: Inventory is empty.', file=sys.stderr)
        cols = ['binder_name', 'page_number', 'slot_number', 'card_id', 'card_name', 'set_id', 'set_name', 'card_number', 'card_market_value', 'index']
        pd.DataFrame(columns=cols).to_csv(output_file, index=False)
        return
    lookup_df = lookup_df[['card_id', 'card_name', 'set_name', 'card_market_value']]
    merged = pd.merge(inventory_df, lookup_df, on=['card_id', 'card_name'], how='left')
    merged['card_market_value'] = merged['card_market_value'].fillna(0.0)
    merged['set_name'] = merged['set_name'].fillna('NOT_FOUND')
    merged['index'] = merged['binder_name'].astype(str) + '_' + merged['page_number'].astype(str) + '_' + merged['slot_number'].astype(str)
    merged.to_csv(output_file, index=False)
    print('Portfolio updated.')

def main():
    update_portfolio('./card_inventory/', './card_set_lookup/', 'card_portfolio.csv')

def test():
    update_portfolio('./card_inventory_test/', './card_set_lookup_test/', 'test_card_portfolio.csv')

if __name__ == "__main__":
    print(f"update_portfolio.py running in Test Mode.", file=sys.stderr)
    test()