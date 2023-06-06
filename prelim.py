import json
import pandas as pd
import time
import config
import psycopg2
from joblib import load
import requests
from random import randint
import threading

class GenesisTradingAPI:
    def __init__(self, token, url):
        self.token = token
        self.base_url = "https://this-is-not-the-real-url-dont-try-to-call-my-api-thanks.herokuapp.com/api"

    def send_trade_signal(self, ticket, symbol, type, sl, tp, volume):
        data = {"ticket": ticket, "symbol": symbol, "type": type, "sl": sl, "tp": tp, "volume": volume}
        url = f"{self.base_url}/signals/add"
        headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": f"Bearer {self.token}"}

        try:
            response = requests.post(url, data=json.dumps(data), headers=headers)
            response.raise_for_status()
            print("Trade signal sent successfully!")
            print(response.json())  # Print the response data
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

def ohcl(pair, period, offset):
    try:
        # Connect to postgres DB
        conn = psycopg2.connect(
            dbname=config.db,
            user=config.user,
            password=config.password,
            host=config.host,
            port=config.port
        )
        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Execute an SQL query
        cur.execute(f"SELECT * FROM {pair} ORDER BY time DESC LIMIT {period} OFFSET {offset}")

        # Retrieve query results
        records = cur.fetchall()

        # Close cursor and connection
        cur.close()
        conn.close()

        # Transform the data into a pandas DataFrame for further processing
        data = pd.DataFrame(records, columns=['open', 'high', 'low', 'close', 'hour', 'time'])

        return data
    except Exception as e:
        print(f"Error fetching data from database for pair {pair}: {e}")
        return None

def load_model(file_name):
    try:
        return load(file_name)
    except Exception as e:
        print(f"Error loading model {file_name}: {e}")
        return None

def load_config(pair):
    try:
        with open(f"../JSONed/{pair}config.json", "r") as json_file:
            return json.load(json_file)
    except Exception as e:
        print(f"Error loading config for {pair}: {e}")
        return None

def process_pair(pair):
    while True:
        hour = (datetime.now().hour - 9) % 24
        minute = datetime.now().minute
        print(f"Processing Pair: {pair}, Minute: {minute}, Hour: {hour}")

        config_dict = load_config(pair)
        if config_dict is None:
            time.sleep(60)
            continue

        sl_value = config_dict.get(f"{hour}.0", {}).get("SL")
        tp_value = config_dict.get(f"{hour}.0", {}).get("TP")

        if minute in [0, 30] and sl_value is not None and tp_value is not None:
            try:
                data = ohcl(pair, 201, 0)
                if data is None:
                    time.sleep(60)
                    continue

                model = load_model(f'../SandBox/Models/{pair}_{hour}.joblib')
                if model is None:
                    time.sleep(60)
                    continue

                data = data.drop(['hour', 'time'], axis=1)
                prediction = model.predict(data)
                close = data['close'].iloc[-1]
                if prediction == 1:
                    api = GenesisTradingAPI(token)
                    ticket = randint(100000, 999999)
                    api.send_trade_signal(ticket=ticket, symbol=pair, type='BUY', sl=(close-(sl_value*1.5)), tp=(close+tp_value), volume=0.1)
                elif prediction == -1:
                    api = GenesisTradingAPI(token)
                    ticket = randint(100000, 999999)
                    api.send_trade_signal(ticket=ticket, symbol=pair, type='SELL', sl=close+(sl_value*1.5), tp=close-tp_value, volume=0.1)

            except Exception as e:
                print(f"Error processing pair {pair}: {e}")

        time.sleep(60)

currency_pairs = ['AUDJPY', 'EURJPY', 'NZDJPY', 'GBPJPY']

for pair in currency_pairs:
    t = threading.Thread(target=process_pair, args=(pair,))
    t.start()
