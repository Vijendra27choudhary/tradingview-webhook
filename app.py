from flask import Flask, request
import pandas as pd
import os

app = Flask(__name__)

# Route to handle incoming TradingView alerts
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # Parse incoming JSON data
    if not data:
        return "No data received", 400

    # Extract the fields from the JSON payload
    extracted_data = {
        'Ticker': data.get('ticker', 'N/A'),
        'Price': data.get('price', 'N/A'),
        'Time': data.get('time', 'N/A'),
        'Volume': data.get('volume', 'N/A'),
    }

    # Define the Excel file path
    file_path = os.path.join(os.getcwd(), 'trading_data.xlsx')

    # Check if the file exists
    if os.path.exists(file_path):
        # Read the existing data into a DataFrame
        df = pd.read_excel(file_path)
    else:
        # Create a new DataFrame if the file doesn't exist
        df = pd.DataFrame(columns=['Ticker', 'Price', 'Time', 'Volume'])

    # Append the new data to the DataFrame
    df = pd.concat([df, pd.DataFrame([extracted_data])], ignore_index=True)

    # Save back to the Excel file
    df.to_excel(file_path, index=False)

    return "Data received and saved", 200

if __name__ == '__main__':
    app.run(debug=False)
