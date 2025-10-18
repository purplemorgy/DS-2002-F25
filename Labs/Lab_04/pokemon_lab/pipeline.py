#!/usr/bin/python3
import sys
import update_portfolio
import generate_summary

def run_production_pipeline():
    print(f"--- Running pipeline ---", file=sys.stderr)
    print("--- Updating portfolio ---")
    update_portfolio.main()
    print("--- Generating portfolio summary ---")
    generate_summary.main()
    print(f"--- Pipeline complete ---", file=sys.stderr)

if __name__ == "__main__":
    run_production_pipeline()