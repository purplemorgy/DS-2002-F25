.PHONY: all fetch analyze clean

analyze: fetch
	@echo "--- Analyzing data ---"
	bash ./analyze_data.sh

fetch:
	@echo "--- Fetching metars ---"
	bash ./fetch_metars.sh

clean:
	@echo "--- Cleaning up ---"
	rm weather_report.csv
	rm -rf raw_metars
