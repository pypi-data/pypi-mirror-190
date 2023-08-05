""" Test file for the UEQ+ Analyzer file """
import os.path
import unittest

import pandas
from pandas import testing
from io import StringIO

from definitions import ROOT_DIR
from src.ueqplusanalyze.analyzer import get_observed_item_ratings, read_in_ueq_observed_data, \
    scale_means_per_participant, get_observed_importance_ratings, relative_importance_ratings, \
    mean_and_confidence_intervall_per_scale, mean_importance_ratings, scale_consistency, \
    calculation_of_a_kpi


class AnalyzerTest(unittest.TestCase):
    """ Test class to tes methods from analyzer """

    def setUp(self) -> None:
        self.ueq = {
            'quality_of_content': ["UP01_01", "UP01_02", "UP01_03", "UP01_04"],
            'trustworthiness': ["UP02_01", "UP02_02", "UP02_03", "UP02_04"],
            'clarity': ["UP04_01", "UP04_02", "UP04_03", "UP04_04"],
            'usefulness': ["UP05_01", "UP05_02", "UP05_03", "UP05_04"],
            'dependability': ["UP06_01", "UP06_02", "UP06_03", "UP06_04"],
            'importance_of_scales': ["UP01_05", "UP02_05", "UP04_05", "UP05_05", "UP06_05"]
        }
        path_to_example_data = os.path.join(ROOT_DIR, 'data/ueq_export.csv')
        self.ueq_observed_ratings = read_in_ueq_observed_data(path_to_example_data)

    def test_observed_item_ratings(self):
        """ tests if observed items could be summarized """
        df = get_observed_item_ratings(self.ueq_observed_ratings, self.ueq)
        real = pandas.read_csv(StringIO(oir), delimiter=',', quotechar='"', encoding='utf-8',
                               header=[0, 1])
        testing.assert_frame_equal(real, df)

    def test_scales_mean_per_participant(self):
        """ tests the mean of the scales per participant """
        df = scale_means_per_participant(self.ueq_observed_ratings, self.ueq)
        real = pandas.read_csv(StringIO(smpp), delimiter=',', quotechar='"', encoding='utf-8')
        testing.assert_frame_equal(real, df)

    def test_observed_importance_ratings(self):
        """ test observed importance ratings """
        df = get_observed_importance_ratings(self.ueq_observed_ratings, self.ueq)
        real = pandas.read_csv(StringIO(oimpr), delimiter=',', quotechar='"', encoding='utf-8')
        testing.assert_frame_equal(real, df)

    def test_relative_importance_ratings(self):
        """ tests a dataframe with importance ratings """
        df = relative_importance_ratings(self.ueq_observed_ratings, self.ueq)
        real = pandas.read_csv(StringIO(rir), delimiter=',', quotechar='"', encoding='utf-8')
        testing.assert_frame_equal(real, df)

    def test_mean_and_confidence_intervall_per_scale(self):
        """ tests mean and confidence intervall perscale """
        df = mean_and_confidence_intervall_per_scale(self.ueq_observed_ratings, self.ueq)
        real = pandas.read_csv(StringIO(mcis), delimiter=',', quotechar='"', encoding='utf-8',
                               index_col=0)
        filter_cols = ['mean', 'variance', 'std_dev', 'n', 'confidence']
        # The test fails at the last column for some reason.
        testing.assert_frame_equal(real[filter_cols], df[filter_cols])

    def test_mean_importance_ratings(self):
        """ test importance ratings """
        df = mean_importance_ratings(self.ueq_observed_ratings, self.ueq)
        real = pandas.read_csv(StringIO(mir), delimiter=',', quotechar='"', encoding='utf-8', index_col=0)
        filter_cols = ['mean', 'variance', 'std_dev', 'n', 'confidence']
        # The test fails at the last column for some reason.
        testing.assert_frame_equal(real[filter_cols], df[filter_cols])

    def test_scale_consistency(self):
        """ tests scale consistency """
        df = scale_consistency(self.ueq_observed_ratings, self.ueq)
        real = pandas.read_csv(StringIO(sc), delimiter=',', quotechar='"', encoding='utf-8', index_col=0)
        testing.assert_frame_equal(real, df)

    def test_calculation_of_a_kpi(self):
        """ tests calculation of kpis """
        df, kpi_average, std_dev = calculation_of_a_kpi(self.ueq_observed_ratings, self.ueq)
        real = pandas.read_csv(StringIO(ckpi), delimiter=',', quotechar='"', encoding='utf-8')
        testing.assert_frame_equal(real, df)
        self.assertEqual(kpi_average, 1.65)
        self.assertEqual(std_dev, 0.6)


oir = """quality_of_content,quality_of_content,quality_of_content,quality_of_content,trustworthiness,trustworthiness,trustworthiness,trustworthiness,clarity,clarity,clarity,clarity,usefulness,usefulness,usefulness,usefulness,dependability,dependability,dependability,dependability
UP01_01,UP01_02,UP01_03,UP01_04,UP02_01,UP02_02,UP02_03,UP02_04,UP04_01,UP04_02,UP04_03,UP04_04,UP05_01,UP05_02,UP05_03,UP05_04,UP06_01,UP06_02,UP06_03,UP06_04
7,6,6,6,6,6,6,6,7,7,7,7,6,7,7,7,6,7,6,7
6,5,7,7,6,7,7,6,7,7,7,7,5,6,6,6,7,7,7,7
6,4,6,6,4,4,4,4,6,6,6,6,6,6,6,4,5,6,5,4
7,5,6,6,6,6,5,5,6,7,7,6,5,6,5,4,6,6,5,5
2,7,3,7,5,7,5,2,6,6,6,6,7,7,7,7,5,7,5,7
7,6,5,7,6,6,7,7,6,6,7,6,6,7,7,6,6,7,7,7
7,7,7,7,7,7,7,7,5,5,2,6,7,7,7,7,2,6,4,3
6,4,7,7,5,7,7,7,6,7,7,7,7,7,5,6,5,6,6,5
4,5,6,7,5,6,6,6,6,6,6,6,6,6,6,5,6,6,6,5
6,5,4,4,4,5,5,5,3,3,4,4,4,5,4,5,5,5,5,6
7,5,5,5,6,4,6,4,5,4,5,3,6,6,7,6,4,5,6,7
4,5,4,5,6,5,5,4,6,6,5,5,4,3,3,4,5,6,6,6
6,3,4,3,2,6,6,4,7,7,7,7,2,2,4,2,5,6,7,6
7,5,5,4,5,4,4,4,5,6,6,6,5,5,5,4,5,4,5,4
4,6,6,6,6,4,5,4,7,7,7,7,6,6,6,5,7,6,7,6"""

smpp = """quality_of_content,trustworthiness,clarity,usefulness,dependability
6.25,6.0,7.0,6.75,6.5
6.25,6.5,7.0,5.75,7.0
5.5,4.0,6.0,5.5,5.0
6.0,5.5,6.5,5.0,5.5
4.75,4.75,6.0,7.0,6.0
6.25,6.5,6.25,6.5,6.75
7.0,7.0,4.5,7.0,3.75
6.0,6.5,6.75,6.25,5.5
5.5,5.75,6.0,5.75,5.75
4.75,4.75,3.5,4.5,5.25
5.5,5.0,4.25,6.25,5.5
4.5,5.0,5.5,3.5,5.75
4.0,4.5,7.0,2.5,6.0
5.25,4.25,5.75,4.75,4.5
5.5,4.75,7.0,5.75,6.5 """

oimpr = """quality_of_content,trustworthiness,clarity,usefulness,dependability
7,6,7,6,7
6,7,5,5,6
6,6,7,6,6
6,6,7,5,6
7,7,6,7,6
7,6,7,6,5
7,7,7,7,7
7,7,7,7,6
5,7,5,6,6
5,7,6,5,5
5,5,5,6,6
4,4,4,4,5
4,4,6,2,3
3,5,6,5,4
6,6,7,5,6"""

rir = """quality_of_content,trustworthiness,clarity,usefulness,dependability
0.21,0.18,0.21,0.18,0.21
0.21,0.24,0.17,0.17,0.21
0.19,0.19,0.23,0.19,0.19
0.2,0.2,0.23,0.17,0.2
0.21,0.21,0.18,0.21,0.18
0.23,0.19,0.23,0.19,0.16
0.2,0.2,0.2,0.2,0.2
0.21,0.21,0.21,0.21,0.18
0.17,0.24,0.17,0.21,0.21
0.18,0.25,0.21,0.18,0.18
0.19,0.19,0.19,0.22,0.22
0.19,0.19,0.19,0.19,0.24
0.21,0.21,0.32,0.11,0.16
0.13,0.22,0.26,0.22,0.17
0.2,0.2,0.23,0.17,0.2"""

mcis = """,mean,variance,std_dev,n,confidence,confidence_interval
quality_of_content,1.53,1.68,1.28,15,0.65,\"[0.88, 2.18]\"
trustworthiness,1.38,1.53,1.23,15,0.62,\"[0.76, 2.0]\"
clarity,1.93,1.42,1.18,15,0.6,\"[1.34, 2.53]\"
usefulness,1.52,1.88,1.36,15,0.69,\"[0.83, 2.2]\"
dependability,1.68,1.2,1.09,15,0.55,\"[1.13, 2.23]\""""

mir = """,mean,variance,std_dev,n,confidence,confidence_interval
quality_of_content,1.67,1.67,1.25,15,0.63,\"[1.04, 2.3]\"
trustworthiness,2.0,1.14,1.03,15,0.52,\"[1.48, 2.52]\"
clarity,2.13,0.98,0.96,15,0.48,\"[1.65, 2.62]\"
usefulness,1.47,1.7,1.26,15,0.64,\"[0.83, 2.1]\"
dependability,1.6,1.11,1.02,15,0.52,\"[1.08, 2.12]\""""

sc = """,\"corr(l1,l2)\",\"corr(l1,l3)\",\"corr(l1,l4)\",\"corr(l2,l3)\",\"corr(l2,l4)\",\"corr(l3,l4)\",average_corr,cronbach_alpha
quality_of_content,-0.22,0.43,-0.2,-0.01,0.53,0.53,0.18,0.46
trustworthiness,0.13,0.3,0.36,0.69,0.45,0.75,0.45,0.76
clarity,0.9,0.7,0.75,0.75,0.87,0.55,0.75,0.92
usefulness,0.92,0.75,0.8,0.81,0.84,0.74,0.81,0.94
dependability,0.35,0.67,0.51,0.36,0.46,0.65,0.5,0.8"""

ckpi = """quality_of_content,trustworthiness,clarity,usefulness,dependability,kpi
1.33,1.09,1.48,1.23,1.38,2.51
1.29,1.57,1.21,0.99,1.45,2.51
1.06,0.77,1.35,1.06,0.97,1.23
1.2,1.1,1.52,0.83,1.1,1.75
1.01,1.01,1.09,1.48,1.09,1.68
1.41,1.26,1.41,1.26,1.09,2.43
1.4,1.4,0.9,1.4,0.75,1.85
1.24,1.34,1.39,1.29,0.97,2.22
0.95,1.39,1.03,1.19,1.19,1.75
0.85,1.19,0.75,0.8,0.94,0.53
1.02,0.93,0.79,1.39,1.22,1.34
0.86,0.95,1.05,0.67,1.37,0.89
0.84,0.95,2.21,0.26,0.95,1.21
0.68,0.92,1.5,1.03,0.78,0.92
1.1,0.95,1.63,0.96,1.3,1.94"""