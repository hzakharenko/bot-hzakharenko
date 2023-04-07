import datasette.app
import uvicorn

db_path = 'open_data_dc.db'
app = datasette.Datasette([db_path])
result = app.serve(port=8001)

url = result.url('')  # The empty string gets the base URL of the instance
print(f"Shareable URL: {url}")