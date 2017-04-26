import unittest

import numpy as np
import pandas as pd

from healthcareai import DevelopSupervisedModel
from healthcareai.tests.helpers import fixture
from healthcareai.common.helpers import count_unique_elements_in_column
from healthcareai.common.healthcareai_error import HealthcareAIError
import healthcareai.pipelines.data_preparation as pipelines

# Set some constants to save errors and typing
CLASSIFICATION = 'classification'
PREDICTED_COLUMN = 'ThirtyDayReadmitFLG'
GRAIN_COLUMN_NAME = 'PatientID'


class TestRFDevTuneFalse(unittest.TestCase):
    def test_random_forest_dev_tune_false(self):
        df = pd.read_csv(fixture('DiabetesClincialSampleData.csv'), na_values=['None'])

        # Drop uninformative columns
        df.drop(['PatientID', 'InTestWindowFLG'], axis=1, inplace=True)

        np.random.seed(42)
        df = pipelines.dataframe_preparation_pipeline(df,
                                                      CLASSIFICATION,
                                                      GRAIN_COLUMN_NAME,
                                                      PREDICTED_COLUMN,
                                                      impute=True)
        o = DevelopSupervisedModel(df, CLASSIFICATION, PREDICTED_COLUMN)

        o.train_test_split()
        o.random_forest(cores=1)

        self.assertAlmostEqual(np.round(o.au_roc, 6), 0.965070)


class TestRFDevTuneTrueRegular(unittest.TestCase):
    def test_random_forest_dev_tune_true_succeeds(self):
        df = pd.read_csv(fixture('DiabetesClincialSampleData.csv'), na_values=['None'])

        # Drop uninformative columns
        df.drop(['PatientID', 'InTestWindowFLG'], axis=1, inplace=True)

        np.random.seed(42)
        df = pipelines.dataframe_preparation_pipeline(df,
                                                      CLASSIFICATION,
                                                      GRAIN_COLUMN_NAME,
                                                      PREDICTED_COLUMN,
                                                      impute=True)
        o = DevelopSupervisedModel(df, CLASSIFICATION, PREDICTED_COLUMN)

        o.train_test_split()
        o.random_forest(cores=1, tune=True)

        self.assertAlmostEqual(np.round(o.au_roc, 6), 0.968028)


class TestRFDevTuneTrue2ColError(unittest.TestCase):
    def test_random_forest_dev_tune_true_2_column_raises_error(self):
        cols = ['ThirtyDayReadmitFLG', 'SystolicBPNBR', 'LDLNBR']
        df = pd.read_csv(fixture('DiabetesClincialSampleData.csv'),
                         na_values=['None'],
                         usecols=cols)

        np.random.seed(42)
        df = pipelines.dataframe_preparation_pipeline(df,
                                                      CLASSIFICATION,
                                                      GRAIN_COLUMN_NAME,
                                                      PREDICTED_COLUMN,
                                                      impute=True)
        o = DevelopSupervisedModel(df, CLASSIFICATION, PREDICTED_COLUMN)

        o.train_test_split()

        self.assertRaises(HealthcareAIError, o.random_forest, cores=1, tune=True)

    def test_random_forest_dev_tune_true_2_column_error_message(self):
        cols = ['ThirtyDayReadmitFLG', 'SystolicBPNBR', 'LDLNBR']
        df = pd.read_csv(fixture('DiabetesClincialSampleData.csv'),
                         na_values=['None'],
                         usecols=cols)

        np.random.seed(42)
        df = pipelines.dataframe_preparation_pipeline(df,
                                                      CLASSIFICATION,
                                                      GRAIN_COLUMN_NAME,
                                                      PREDICTED_COLUMN,
                                                      impute=True)
        o = DevelopSupervisedModel(df, CLASSIFICATION, PREDICTED_COLUMN)

        o.train_test_split()

        try:
            o.random_forest(cores=1, tune=True)
            # Fail the test if the above call doesn't throw an error
            self.fail()
        except HealthcareAIError as e:
            self.assertEqual(e.message, 'You need more than two columns to tune hyperparameters.')


class TestLinearDevTuneFalse(unittest.TestCase):
    def test_linear_dev_tune_false(self):
        df = pd.read_csv(fixture('DiabetesClincialSampleData.csv'), na_values=['None'])

        # Drop uninformative columns
        df.drop(['PatientID', 'InTestWindowFLG'], axis=1, inplace=True)

        np.random.seed(42)
        df = pipelines.dataframe_preparation_pipeline(df,
                                                      CLASSIFICATION,
                                                      GRAIN_COLUMN_NAME,
                                                      PREDICTED_COLUMN,
                                                      impute=True)
        o = DevelopSupervisedModel(df, CLASSIFICATION, PREDICTED_COLUMN)

        o.train_test_split()
        o.linear(cores=1)

        self.assertAlmostEqual(np.round(o.au_roc, 3), 0.672000)


class TestHelpers(unittest.TestCase):
    def test_class_counter_on_binary(self):
        df = pd.read_csv(fixture('DiabetesClincialSampleData.csv'), na_values=['None'])
        df.dropna(axis=0, how='any', inplace=True)
        result = count_unique_elements_in_column(df, 'ThirtyDayReadmitFLG')
        self.assertEqual(result, 2)

    def test_class_counter_on_many(self):
        df = pd.read_csv(fixture('DiabetesClincialSampleData.csv'), na_values=['None'])
        result = count_unique_elements_in_column(df, 'PatientEncounterID')
        self.assertEqual(result, 1000)


if __name__ == '__main__':
    unittest.main()
