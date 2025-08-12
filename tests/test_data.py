import csv
import unittest
from src.record import Record
from collections import deque
import pandas as pd
import numpy as np

class TestRecord(unittest.TestCase):
    def setUp(self):
        # Sample DataFrame for testing
        max_records=201
        buffer = deque(maxlen=max_records)
        with open('tests/test.csv', mode='r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    buffer.append(row)
                    self.df = pd.DataFrame(buffer)

    def test_record_initialization(self):
        record = Record(self.df)
        print(str(record))
        self.assertIsNotNone(record)
        self.assertEqual(record.SMA_200, np.float64(1.05926305))
        self.assertEqual(record.SMA_50, np.float64(1.0607838))
        self.assertEqual(record.SMA_50_PREV, np.float64(1.0613633999999998))
        self.assertEqual(record.SMA_20, np.float64(1.0470735))
        self.assertEqual(record.SMA_20_PREV, np.float64(1.0479125))
        self.assertEqual(record.VA_20, np.float64(41685.70329))
        self.assertEqual(record.RSI_14, np.float64(41.583983218600004))
        self.assertEqual(record.OPEN, 1.04425)
        self.assertEqual(record.HIGH, 1.04942)
        self.assertEqual(record.LOW, 1.0424)
        self.assertEqual(record.CLOSE, 1.04663)
        self.assertEqual(record.VOLUME, 85410.23)
        self.assertEqual(record.TIMESTAMP, "2022-06-15 04:00:00+00:00")
        self.assertEqual(record.MACD, np.float64(-0.005178685736807465))
        self.assertEqual(record.MACD_signal, np.float64(-0.005950397369620958))
        self.assertEqual(record.MACD_diff, np.float64(0.000771711632813493))
        self.assertEqual(record.MACD_diff_PREV, np.float64(0.0004211275878219572))
