from enum import Enum

import pandas as pd
from finta import TA


class Signal(Enum):
  BUY = 0
  SELL = 1
  HOLD = 2


def calc_SMA(dataFrame: pd.DataFrame, period: int = 14) -> Signal:
    """calculate technical indicator
    Args:
      dataFrame (pd.DataFrame): ohlc data
      period (int):  Defaults to 14.
    Returns:
      Signal:
    """
    # SMA = ta.SMA(dataFrame['Close'],period)
    TA.SMA(dataFrame, period)
    return Signal.BUY

def calc_EMA(dataFrame: pd.DataFrame, period: int = 14) -> Signal:
    """calculate technical indicator
    Args:
        dataFrame (pd.DataFrame): ohlc data
        period (int):  Defaults to 14.
    Returns:
        Signal: 
    """
    TA.EMA(dataFrame, period)
    return Signal.SELL