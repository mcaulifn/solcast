=========
pysolcast
=========

| |Build Status| |CodeCov| |pypi| |codeclimate|




Solcast API

Client library for interacting with the Solcast API

Basic Usage
-----------

.. code-block:: python

    from pysolcast.rooftop import RooftopSite
    
    site = RooftopSite(api_key, resource_id)
    forecasts = site.get_forecasts()


Full API Documentation_.

.. _Documentation: https://docs.solcast.com.au


.. |Build Status| image:: https://github.com/mcaulifn/solcast/workflows/build/badge.svg
   :target: https://github.com/mcaulifn/solcast

.. |CodeCov| image:: https://codecov.io/gh/mcaulifn/solcast/branch/master/graph/badge.svg?token=04NTIH61T2
  :target: https://codecov.io/gh/mcaulifn/solcast

.. |pypi| image:: https://badge.fury.io/py/pysolcast.svg
    :target: https://badge.fury.io/py/pysolcast

.. |codeclimate| image:: https://api.codeclimate.com/v1/badges/670e0a037d968b173393/maintainability
   :target: https://codeclimate.com/github/mcaulifn/solcast/maintainability
   :alt: Maintainability
