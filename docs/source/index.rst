Welcome to Artiq Iseg HV PSU's documentation!
=============================================

How to run::

    $ aqctl_artiq_iseg_hv_psu.py -d device_ip

Then, send commands to it via the ``sipyco_rpctool`` utility::

    $ sipyco_rpctool 127.0.0.1 3280 call set_channel_voltage ${channel} ${voltage}

API
---

.. automodule:: artiq_iseg_hv_psu.driver
    :members:


ARTIQ Controller
----------------

.. argparse::
   :ref: artiq_iseg_hv_psu.aqctl_artiq_iseg_hv_psu.get_argparser
   :prog: aqctl_artiq_iseg_hv_psu

