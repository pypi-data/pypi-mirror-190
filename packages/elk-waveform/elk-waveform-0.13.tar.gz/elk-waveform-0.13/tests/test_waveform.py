"""
Implements tests for the waveform classes.
"""

import unittest
import numpy as np
import numpy.testing as npt
from elk.waveform import Timeseries

class TestWaveforms(unittest.TestCase):
    def setUp(self):
        """Run setup before each test."""
        self.numpy_data = np.random.rand(100)
        self.numpy_variance = np.random.rand(100)
        self.numpy_times = np.linspace(0, 1, 100)

    def test_data_only_numpy(self):
        """[numpy] Test a timeseries which only has data."""
        timeseries = Timeseries(data=self.numpy_data,
                                times=self.numpy_times)

        npt.assert_array_equal(self.numpy_data, timeseries.data)
        self.assertAlmostEqual(timeseries.dt,  0.010101010101)

    def test_multiplication(self):
        """[numpy] Test that multiplying a timeseries by a scalar works."""
        timeseries = Timeseries(data=self.numpy_data,
                                times=self.numpy_times)
        npt.assert_array_equal(self.numpy_data*2, (timeseries*2).data)

    def test_frequencyseriesconversion(self):
        """[numpy] Convert a timeseries to a frequency series."""
        timeseries = Timeseries(data=self.numpy_data,
                                times=self.numpy_times,
                                variance=self.numpy_variance
        )
        freqseries = timeseries.to_frequencyseries()
        self.assertEqual(len(freqseries), 1+0.5*len(timeseries))
        self.assertEqual(len(freqseries.variance), 1+0.5*len(timeseries.variance))
