# Positions-by-sectors-binance

# Binance Position Tracker

## Overview
This Python project is a positions tracker and calculates delta of your futures positions and divide it by sectors.

## Features
- Retrieves current positions in both futures and spot markets
- Calculates the USD value of each spot position
- Classifies futures positions as either long or short
- Summarizes total size and unrealized profit/loss (PnL) of futures positions
- Divides futures positions into BTC/ETH and ALTs categories
- Classifies futures positions based on predefined sectors
- Outputs data to an Excel spreadsheet

## Requirements
- Python 3.6 or later
- Binance API Key and Secret Key
- Required Python packages: pandas, binance.client, dotenv

## Setup

1. Clone this repository.
2. Install the required Python packages if you haven't already:
pip install python-binance python-dotenv pandas
3. Set up your Binance API Key and Secret Key as environment variables. The keys should be saved in a .env file in the project root directory as follows:

## Usage
Run the main script from your terminal:

The script will print the positions and balance information to the console and also output an Excel spreadsheet ("positions21.xlsx") in the project directory. 

below is the example of an output

<img width="1528" alt="Screenshot 2023-06-16 at 18 59 52" src="https://github.com/BobbyAxer/Positions-by-sectors-binance/assets/81931426/71c01b0c-21b5-4da2-8dfd-f7791233d5af">

<img width="1648" alt="Screenshot 2023-06-16 at 19 00 49" src="https://github.com/BobbyAxer/Positions-by-sectors-binance/assets/81931426/9f6afb73-097e-4ccd-a119-b79a4f3ac813">
