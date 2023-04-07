pip install sqlite-utils
pip install datasette
sqlite-utils insert open_data_dc.db datasets final_df.csv --csv
datasette serve open_data_dc.db