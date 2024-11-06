Agent Overview:
The mdaniels33_finalagentMPD trading agent operates within the ABIDES simulation framework, focusing on high-frequency trading strategies for the asset JPM. It primarily uses the Relative Strength Index (RSI) to inform its trading decisions and applies a fixed stop-loss strategy to manage risk effectively.

RSI Trading Strategy:
The agent employs RSI, a widely recognized momentum oscillator, to discern potential trading opportunities. An RSI reading below 20 is interpreted as an oversold condition, suggesting a favorable moment for the agent to initiate buy orders, provided sufficient cash reserves are available. On the flip side, an RSI value exceeding 80 is perceived as an overbought scenario, compelling the agent to execute sell orders or engage in short selling. RSI calculations are derived from the asset's historical closing prices, adhering to a predefined look-back period.

The Relative Strength Index (RSI) is a momentum oscillator that measures the speed and magnitude of recent price changes to evaluate overbought or oversold conditions in the price of an asset. To calculate the RSI, one typically follows these steps: First, determine the average gains and average losses over a specified period. This is done by comparing the closing price of each period to the previous period's closing price, recording the change as a gain if the price increased, or as a loss if it decreased. If there's no change, both gain and loss are zero. Second, calculate the relative strength (RS) which is the ratio of the average gain to the average loss over the period. Finally, the RSI is calculated using the formula: RSI = 100 - (100 / (1 + RS)). This formula yields a value between 0 and 100, indicating whether a security might be considered overbought (RSI above 80) or oversold (RSI below 20), suggesting potential reversal points in the market.

Fixed Stop-Loss Strategy:
In contrast to dynamic adjustments based on market volatility, the agent adopts a fixed stop-loss approach to safeguard its positions. Specifically, for long positions, the stop-loss threshold is determined by setting the stop price at 90% (0.9 times) of the purchase price. Conversely, for short positions, the stop price is established at 110% (1.1 times) of the sale price. This strategy is straightforward yet effective in curtailing potential losses by automatically triggering sell or buy-back orders when these predefined thresholds are crossed.

Implementation Details:

Initialization: The agent is initialized with a set cash balance, and predefined size for each trade, alongside a wake-up frequency to evaluate market conditions periodically.
Market Analysis: With each wake-up call, the agent computes the current RSI based on recent price movements and assesses the need to trade based on the RSI readings.
Trade Execution: Leveraging the RSI signals, the agent executes trades while adhering to the fixed stop-loss thresholds. It meticulously ensures the closure of all open positions by the trading day's end, aligning with the project's stipulations.
