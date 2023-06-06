# Multi-model Currency Trading Machine Learning Implementation
This repository contains an example of a machine learning implementation for multi-model currency trading. 
It serves as an extremely simplified representation of an outdated version of a larger, closed-source quantitative trading project that has been in development for several years.

## About the project
This script is a part of a more comprehensive and complex project that is entirely automated. The full project pulls data via web scraping, APIs, and many other resources. It uses advanced techniques such as Natural Language Processing (NLP), clustering, Long Short-Term Memory (LSTM) networks, and other machine learning methodologies, all working in harmony.

Post this initial step, there are numerous 'gatekeepers' involved that either veto or approve the trade, based on a series of checks and balances, including risk management strategies and watch-dog algorithms. All these mechanisms work together to ensure the robustness and reliability of the trading system.

This project has been a solo endeavor and, as such, has been under development for quite some time. The full implementation has yet to be run with any substantial amounts of real money and has primarily been restricted to paper trading.

Some of the key challenges that need to be addressed before the system can be safely deployed include latency issues among others. The work is ongoing to refine and enhance the trading system further.

## About this code
This project is a multi-threaded Python script designed to pull financial data from a PostgreSQL database, feed it into several trained LSTM models, and then use those models to make trading decisions for multiple currency pairs. These decisions are then sent as signals to a custom-built API, which acts as an intermediary and sends the trade to a C++ script to be executed on a MetaTrader terminal.

Please note that the API, C++ script, MetaTrader terminal, and various other elements of the complete system are not included in this repository.

This script is watch-dogged by another script that is also not present in this repository. Furthermore, there are no risk management strategies or hedging techniques coded into this simplified script.

The code provided in this repository is not meant to be run as-is. It will not work due to missing parameters, dependencies, and required files. It is a simplified version of a larger, more complex system.

## Disclaimer
This code is provided as a learning resource and a glimpse into the world of quantitative trading using machine learning. It is not intended to be replicated or used for actual trading. Trading currencies involves substantial risk and is not suitable for everyone. This code does not offer any advice on trading strategies or risk management.

Always use professional financial advice when dealing with real money investments and never risk more than you are willing to lose.

## contributions

This project is not open to contributions, as it serves as a simplified example of a larger, closed-source project. If you have any questions or discussions, feel free to open an issue.
