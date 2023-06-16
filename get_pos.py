import os
import time
from datetime import datetime
import pandas as pd
from sectors import sectors
from binance.client import Client
from dotenv import load_dotenv
load_dotenv()

api_key_binance = os.environ.get('API')
api_secret_binance = os.environ.get('SECRET')
client = Client(api_key_binance, api_secret_binance)




def get_spot_balances(client):
    account = client.get_account()
    balances = account["balances"]
    products = client.get_all_tickers()

    spot_positions = {}
    coin_prices = {}
    for row in products:
        ticker = row["symbol"].replace("USDT", "")
        price = float(row["price"])   # usd

        coin_prices[ticker] = price

    for balance in balances:
        coin = balance["asset"]
        coin_balance = float(balance["free"])

        if coin_balance > 0:
            if coin in coin_prices.keys() or coin in ["USDT", "USDC", "BUSD"]:

                if coin in ["USDT", "USDC", "BUSD"]:
                    usd_value = coin_balance
                else:
                    price = coin_prices[coin]
                    usd_value = round(coin_balance * price, 2)

                if usd_value > 5:
                    spot_positions[coin] = {"coin_amount": coin_balance, "usd_value": usd_value}

    return spot_positions

def get_positions():
    Position_Information = client.futures_position_information()
    positions = [str(i['symbol']) for i in Position_Information if float(i['positionAmt']) != 0]
    side = ["LONG" if float(i['positionAmt']) > 0 else "SHORT" for i in Position_Information if
           float(i['positionAmt']) != 0]

    size = [float(i['notional']) for i in Position_Information if float(i['positionAmt']) != 0]
    pnl = [float(i['unRealizedProfit']) for i in Position_Information if float(i['positionAmt']) != 0]

    long_positions = side.count("LONG")
    short_positions = side.count("SHORT")
    print(f"Number of long positions: {long_positions}")
    print(f"Number of short positions: {short_positions}")
    coin_side = dict(zip(positions, side))
    long_coins = [coin for coin, side in coin_side.items() if side == 'LONG']
    short_coins = [coin for coin, side in coin_side.items() if side == 'SHORT']

    print("Long positions: ", long_coins)
    print("Short positions: ", short_coins)

    df = pd.DataFrame(list(zip(positions, side, size, pnl)),
                      columns =['Symbol', 'Side', 'USD SIZE', 'PnL'])
    print(df)
    total_size = df['USD SIZE'].sum()
    total_pnl = df['PnL'].sum()
    print(f"Total size: {total_size}")
    print(f"Total PnL: {total_pnl}")
    delta = df['USD SIZE'].sum()
    df.loc['Total'] = df.sum(numeric_only=True, axis=0)
    delta_btc_eth = df[(df["Symbol"] == 'ETHBUSD') | (df["Symbol"] == 'BTCUSDT') | (df["Symbol"] == 'BTCBUSD') | (df["Symbol"] == 'ETHUSDT')]['USD SIZE'].sum()
    delta_alt = delta - delta_btc_eth
    print(f'total delta is {delta} delta btc-eth is {delta_btc_eth} delta alts is {delta_alt}')
    df.to_excel('positions21.xlsx', sheet_name='Position_management')

    # Get balance
    balance_info = client.futures_account_balance()
    balances = {asset['asset']: float(asset['balance']) for asset in balance_info}
    print("Balances:", balances)
    balance_spot = get_spot_balances(client)
    print(balance_spot)
    sector_deltas = {}
    for sector, symbols in sectors.items():
        sector_df = df[df['Symbol'].isin(symbols)]
        sector_delta = sector_df['USD SIZE'].sum()
        sector_deltas[sector] = sector_delta

    for sector, delta in sector_deltas.items():
        print(f'Delta for {sector} sector: {delta}')
    return df

get_positions()