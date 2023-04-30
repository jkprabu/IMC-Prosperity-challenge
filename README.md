# IMC Prosperity Trading Challenge

Repository containing the code from IMC Prosperity's challenge. \
**Team's final rank:** 354 out of 7169. 

## Background:
Prosperity is a global (simulated)trading competetion hosted by IMC, with the objective for the participating teams to leverage data analysis and quantitative trading to make the most money (seashells in this case).

The competetion consisted of 5 rounds, each with new commodities with different behaviours. 

## Our strategy:
### Round 1:
We were introduced with 2 commodities, ``PEARLS`` and ``BANANAS``. ``PEARLS`` had a steady price of about 10,000 seashells, and ``BANANAS`` was a highly volatile commodity. 

``PEARL`` & ``BANANA`` : Buy the lowest bid available at any time, and sell it to highest ask.

### Round 2:
We were introduced to 2 new commodities, ``COCONUTS`` and ``PINA_COLADAS``.

``BANANA`` & ``COCONUTS`` & ``PINA_COLADAS``: Implemented a SMA (34) trading strategy. If current price crosses SMA to the upside then buy, if current price crosses SMA to the downside then sell.
$$SMA = \frac{A_1 + A_2 + A_3 + ... + A_{33} + A_{34}}{34}$$

### Round 3, 4 & 5:
Changed the SMA and current price crossover, for MA crossover between 34 MA and 144 MA. 

## Contents:
``visualizer.py``: Visualizer for our startegy. \
``duo.py``: Updated trading algo. \
``testing.py``: Test to check if the algorithm file runs before submittion. 
