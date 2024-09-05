import sys

from sipyco.test.generic_rpc import GenericRPCCase


class GenericTdcTest:
    def test_set_channel_voltage(self):
        voltage = 5e6
        channel = 3
        self.artiq_iseg_hv_psu.set_channel_voltage(channel, voltage)
        self.assertEqual(voltage, self.artiq_iseg_hv_psu.get_channel_voltage(channel))
        self.assertAlmostEqual(
            voltage, self.artiq_iseg_hv_psu.get_channel_voltage(channel), delta=0.5
        )

    def test_set_channel_current(self):
        current = 3e6
        channel = 6
        self.artiq_iseg_hv_psu.set_channel_current(channel, current)
        self.assertEqual(current, self.artiq_iseg_hv_psu.get_channel_current(channel))
        self.assertAlmostEqual(
            current, self.artiq_iseg_hv_psu.get_channel_current(channel), delta=0.5
        )

    def test_set_channel_on(self):
        channel_on = True
        channel = 5
        self.artiq_iseg_hv_psu.set_channel_on(channel, channel_on)
        self.assertEqual(channel_on, self.artiq_iseg_hv_psu.get_channel_on(channel))


class TestTdcSim(GenericRPCCase, GenericTdcTest):
    def setUp(self):
        GenericRPCCase.setUp(self)
        command = (
            sys.executable.replace("\\", "\\\\")
            + " -m artiq_iseg_hv_psu.aqctl_artiq_iseg_hv_psu"
            + " -p 3280 --simulation"
        )
        self.artiq_iseg_hv_psu = self.start_server("artiq_iseg_hv_psu", command, 3280)
