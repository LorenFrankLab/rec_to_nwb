import os
from unittest import TestCase
from pathlib import Path
from testfixtures import should_raise
from rec_to_nwb.processing.validation.ntrode_validator import NTrodeValidator
from rec_to_nwb.processing.header.module import header
from rec_to_nwb.processing.exceptions.invalid_header_exception import InvalidHeaderException
from rec_to_nwb.processing.exceptions.invalid_metadata_exception import InvalidMetadataException

path = os.path.dirname(os.path.abspath(__file__))


class TestNTrodeValidator(TestCase):

    def setUp(self):
        parent_path = str(Path(path).parent)
        res_path = parent_path + '/res/fl_lab_sample_header.xml'
        self.header = header.Header(res_path)

    def test_should_validate_ndtrodes_num_correct(self):

        metadata = {"ntrode electrode group channel map": [
            {"ntrode_id": 1, "electrode_group_id": 0, "bad_channels": [0, 2], "map": {0: 0, 1: 1, 2: 2, 3: 3}},
            {"ntrode_id": 2, "electrode_group_id": 0, "bad_channels": [0, 1], "map": {0: 4, 1: 5, 2: 6, 3: 7}},
        ]}

        validator = NTrodeValidator(metadata, self.header)

        result = validator.create_summary()

        self.assertTrue(result.is_valid())

    def test_should_validate_ndtrodes_num_incorrect_less_than_spikes(self):
        metadata = {"ntrode electrode group channel map": [
            {"ntrode_id": 1, "electrode_group_id": 0, "bad_channels": [0, 2], "map": {0: 0, 1: 1, 2: 2, 3: 3}}]}

        validator = NTrodeValidator(metadata, self.header)
        result = validator.create_summary()

        self.assertFalse(result.is_valid())
        self.assertEqual(result.ntrodes_num, 1)

    def test_should_validate_ndtrodes_num_incorrect_greater_than_spikes(self):

        metadata = {"ntrode electrode group channel map": [
            {"ntrode_id": 1, "electrode_group_id": 0, "bad_channels": [0, 2], "map": {0: 0, 1: 1, 2: 2, 3: 3}},
            {"ntrode_id": 2, "electrode_group_id": 0, "bad_channels": [0, 1], "map": {0: 4, 1: 5, 2: 6, 3: 7}},
            {"ntrode_id": 3, "electrode_group_id": 0, "bad_channels": [0, 2], "map": {0: 8, 1: 9, 2: 10, 3: 11}},
        ]}

        validator = NTrodeValidator(metadata, self.header)
        result = validator.create_summary()

        self.assertFalse(result.is_valid())
        self.assertEqual(result.ntrodes_num, 3)

    @should_raise(InvalidHeaderException)
    def test_should_fail_due_to_empty_header(self):

        metadata = {"ntrode electrode group channel map": [
            {"ntrode_id": 1, "electrode_group_id": 0, "bad_channels": [0, 2], "map": {0: 0, 1: 1, 2: 2, 3: 3}},
            {"ntrode_id": 2, "electrode_group_id": 0, "bad_channels": [0, 1], "map": {0: 4, 1: 5, 2: 6, 3: 7}},
            {"ntrode_id": 3, "electrode_group_id": 0, "bad_channels": [0, 2], "map": {0: 8, 1: 9, 2: 10, 3: 11}},
        ]}

        validator = NTrodeValidator(metadata, None)

        result = validator.create_summary()

    @should_raise(InvalidHeaderException)
    def test_should_fail_due_to_header_without_spike_ntrodes(self):
        metadata = {"ntrode electrode group channel map": [
            {"ntrode_id": 1, "electrode_group_id": 0, "bad_channels": [0, 2], "map": {0: 0, 1: 1, 2: 2, 3: 3}},
            {"ntrode_id": 2, "electrode_group_id": 0, "bad_channels": [0, 1], "map": {0: 4, 1: 5, 2: 6, 3: 7}},
            {"ntrode_id": 3, "electrode_group_id": 0, "bad_channels": [0, 2], "map": {0: 8, 1: 9, 2: 10, 3: 11}},
        ]}

        validator = NTrodeValidator(metadata, self.header)
        self.header.configuration.spike_configuration.spike_n_trodes = None
        result = validator.create_summary()

    def test_should_not_validate_as_there_are_no_ntrodes(self):
        metadata = {"ntrode electrode group channel map": [
            {"ntrode_id": 1, "electrode_group_id": 0, "bad_channels": [0, 2], "map": {0: 0, 1: 1, 2: 2, 3: 3}}
        ]}

        validator = NTrodeValidator(metadata, self.header)
        result = validator.create_summary()

        self.assertFalse(result.is_valid())

    @should_raise(InvalidMetadataException)
    def test_should_fail_due_to_metadata_without_ntrodes(self):

        metadata = {"ntrode electrode group channel map": []}

        validator = NTrodeValidator(metadata, self.header)
        self.header.configuration.spike_configuration.spike_n_trodes = None
        result = validator.create_summary()