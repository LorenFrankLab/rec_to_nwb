from unittest import TestCase
from unittest.mock import Mock

from ndx_franklab_novela.probe import Probe
from pynwb.device import Device
from testfixtures import should_raise

from src.datamigration.exceptions.none_param_in_init_exception import NoneParamInInitException
from src.datamigration.nwb.components.electrode_group.fl_electrode_group_creator import FlElectrodeGroupCreator
from src.datamigration.nwb.components.electrode_group.lf_fl_electrode_group import LfFLElectrodeGroup


class TestFlElectrodeGroupCreator(TestCase):

    def test_creator_create_FLElectrodeGroup_successfully(self):
        mock_probe = Mock(spec=Probe)
        mock_device = Mock(spec=Device)

        mock_lf_fl_electrode_group_1 = Mock(spec=LfFLElectrodeGroup)
        mock_lf_fl_electrode_group_1.device = mock_probe
        mock_lf_fl_electrode_group_1.metadata = {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5',
                                                     'description': 'ElectrodeGroup 1'}

        mock_lf_fl_electrode_group_2 = Mock(spec=LfFLElectrodeGroup)
        mock_lf_fl_electrode_group_2.device = mock_device
        mock_lf_fl_electrode_group_2.metadata = {'id': 1, 'location': 'mPFC',
                                                     'device_type': '128c-4s8mm6cm-20um-40um-sl',
                                                     'description': 'ElectrodeGroup 2'}

        fl_electrode_group_1 = FlElectrodeGroupCreator.create(mock_lf_fl_electrode_group_1)
        fl_electrode_group_2 = FlElectrodeGroupCreator.create(mock_lf_fl_electrode_group_2)
        
        self.assertIsNotNone(fl_electrode_group_1)
        self.assertIsNotNone(fl_electrode_group_2)

        self.assertEqual(fl_electrode_group_1.name, 'electrode group 0')
        self.assertEqual(fl_electrode_group_1.location, 'mPFC')
        self.assertEqual(fl_electrode_group_1.description, 'ElectrodeGroup 1')
        self.assertEqual(fl_electrode_group_1.id, 0)
        self.assertEqual(fl_electrode_group_1.device, mock_probe)

        self.assertEqual(fl_electrode_group_2.name, 'electrode group 1')
        self.assertEqual(fl_electrode_group_2.location, 'mPFC')
        self.assertEqual(fl_electrode_group_2.description, 'ElectrodeGroup 2')
        self.assertEqual(fl_electrode_group_2.id, 1)
        self.assertEqual(fl_electrode_group_2.device, mock_device)

    @should_raise(NoneParamInInitException)
    def test_creator_failed_creating_ElectrodeGroup_due_to_lack_of_FLElectrodeGroup(self):
        FlElectrodeGroupCreator.create(None)

    @should_raise(NoneParamInInitException)
    def test_creator_failed_creating_ElectrodeGroup_due_to_lack_of_FLElectrodeGroup_attr(self):
        mock_lf_fl_electrode_group_1 = Mock(spec=LfFLElectrodeGroup)
        mock_lf_fl_electrode_group_1.device = None
        mock_lf_fl_electrode_group_1.metadata = {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5',
                                                 'description': 'ElectrodeGroup 1'}

        FlElectrodeGroupCreator.create(mock_lf_fl_electrode_group_1)