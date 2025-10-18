#!/usr/bin/python3
import os
import sys
import pandas as pd

def generate_summary(portfolio_file):
    if not os.path.exists(portfolio_file):
        print(f"Portfolio file does not exist.", file=sys.stderr)
        sys.exit(1)
    df = pd.read_csv(portfolio_file)
    if df.empty:
        print("Portfolio file contains no data.")
        return
    total_portfolio_value = df['card_market_value'].sum()
    most_valuable_card = df.loc[df['card_market_value'].idxmax()]
    print(f"Total Portfolio Value: ${total_portfolio_value:,.2f}")
    print(f"Most Valuable Card: {most_valuable_card['card_name']} | ID: {most_valuable_card['card_id']} | Value: ${most_valuable_card['card_market_value']:,.2f}")
    
def main():
    generate_summary('card_portfolio.csv')
def test():
    generate_summary('test_card_portfolio.csv')

if __name__ == "__main__":
    test()
