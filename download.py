from datetime import datetime
import dukascopy_python
from dukascopy_python.instruments import INSTRUMENT_FX_MAJORS_EUR_USD

df = dukascopy_python.fetch(
    instrument=INSTRUMENT_FX_MAJORS_EUR_USD,
    interval=dukascopy_python.INTERVAL_MIN_5,
    offer_side=dukascopy_python.OFFER_SIDE_BID,
    start=datetime(2025, 7, 1),
    end=datetime(2025, 8, 1)
)
df.to_csv('resources/EUR-USD_Minute_2025-07-01_to_2025-08-01.csv', index=True, encoding='utf-8')