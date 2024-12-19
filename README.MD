# mdaniels33_finalagentMPD Trading Agent

## Overview
The **mdaniels33_finalagentMPD** trading agent operates within the ABIDES simulation framework, focusing on high-frequency trading strategies for the asset *JPM*. The agent leverages the **Relative Strength Index (RSI)** for decision-making and implements a **fixed stop-loss strategy** to manage risk effectively. It is designed to align with project requirements, including closing all open positions by the end of each trading day.

---

## Strategy Details

### RSI Trading Strategy
The agent employs the **Relative Strength Index (RSI)**, a momentum oscillator, to identify overbought and oversold conditions in the market:
- **Oversold Condition (RSI < 20)**:
  - Indicates a potential buying opportunity.
  - The agent places buy orders if sufficient cash is available.
- **Overbought Condition (RSI > 80)**:
  - Suggests a potential selling or short-selling opportunity.
  - The agent places sell or short-sell orders accordingly.

#### RSI Calculation
1. **Determine Average Gains and Losses**:
   - Compare the closing prices over a predefined period.
   - Calculate changes as gains (if the price increased) or losses (if the price decreased). No change results in both gain and loss being zero.
2. **Calculate Relative Strength (RS)**:
   - RS = (Average Gain) / (Average Loss).
3. **Calculate RSI**:
   - RSI = 100 - (100 / (1 + RS)).
   - The RSI ranges between 0 and 100:
     - **RSI > 80**: Overbought, indicating a potential reversal.
     - **RSI < 20**: Oversold, suggesting a buying opportunity.

### Fixed Stop-Loss Strategy
The agent adopts a **fixed stop-loss** approach to limit potential losses:
- **Long Positions**:
  - Stop-loss threshold is set at **90% of the purchase price** (0.9 × purchase price).
- **Short Positions**:
  - Stop-loss threshold is set at **110% of the sale price** (1.1 × sale price).

This straightforward strategy ensures automated execution of sell or buy-back orders when prices cross these thresholds.

---

## Implementation Details

### Initialization
- The agent starts with:
  - A predefined cash balance.
  - A fixed trade size for each transaction.
  - A set wake-up frequency to evaluate market conditions periodically.

### Market Analysis
- At each wake-up event:
  - The agent computes the current RSI using recent price movements.
  - Trades are initiated or adjusted based on RSI signals and stop-loss thresholds.

### Trade Execution
- Trades are executed based on the RSI signals:
  - Buy, sell, or short-sell orders are placed.
- Stop-loss levels are continuously monitored and triggered as needed.
- All open positions are closed by the end of the trading day to comply with project requirements.

---

## Files

1. **`mdaniels33_finalagentMPD.py`**:
   - Contains the code implementation of the trading agent.
   - Includes logic for market analysis, RSI calculation, and trade execution.

2. **`finalagentMPD.cfg`**:
   - Configuration file specifying:
     - Initial cash balance.
     - Trade size.
     - Wake-up frequency.
     - Other agent-specific parameters.

---

## How to Use

### Prerequisites
- Install the **ABIDES** simulation framework: [ABIDES GitHub Repository](https://github.com/abides-sim/abides).
- Ensure the asset data for *JPM* is available in the simulation environment.

### Steps
1. Place the files `mdaniels33_finalagentMPD.py` and `finalagentMPD.cfg` in the appropriate directory within the ABIDES framework.
2. Update the `finalagentMPD.cfg` file with desired parameters (e.g., initial cash balance, trade size).
3. Run the agent using the ABIDES simulation framework:
   ```bash
   python abides.py -c finalagentMPD.cfg
