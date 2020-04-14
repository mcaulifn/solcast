=========
pysolcast
=========

| |Build Status| |CodeCov|




Solcast API

Client library for interacting with the Solcast API

Basic Usage
-----------

.. code-block:: python

    from pysolcast import RooftopSite
    
    site = RooftopSite(api_key, resource_id)
    forecasts = site.get_forecasts()


Full API Documentation_.

.. _Documentation: https://docs.solcast.com.au


.. |Build Status| image:: https://github.com/mcaulifn/solcast/workflows/build/badge.svg
   :target: https://github.com/mcaulifn/solcast

.. |CodeCov| image:: https://codecov.io/gh/mcaulifn/solcast/branch/master/graph/badge.svg?token=04NTIH61T2
  :target: https://codecov.io/gh/mcaulifn/solcast
