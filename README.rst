=======
solcast
=======

| |Build Status|




Solcast API

Client library for interacting with the Solcast API

Basic Usage
-----------

.. code-block:: python

    from solcast import RooftopSite
    
    site = RooftopSite(api_key, resource_id)
    forecasts = site.get_forecasts()


Full API Documentation_.

.. _Documentation: https://docs.solcast.com.au


.. |Build Status| image:: https://github.com/mcaulifn/solcast/workflows/main/badge.svg
   :target: https://github.com/mcaulifn/solcast
