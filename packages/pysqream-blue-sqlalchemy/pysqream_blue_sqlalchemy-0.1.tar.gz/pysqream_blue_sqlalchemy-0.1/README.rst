**********************************
SQLAlchemy Dialect for SQream DB
**********************************

Requirements
=====================

* Python > 3.7. Python 3.8.1+ recommended
* SQLAlchemy > 1.3.18
* SQream Blue DB-API Connector >= 1.0.22

Installation
=====================

Install from the PyPi repository using `pip`:

.. code-block:: bash

    pip install --upgrade pysqream_blue_sqlalchemy

Usage
===============================

Integrating with SQLAlchemy
----------------------------

.. code-block:: python

    import sqlalchemy as sa
    conn_string = 'sqream_blue://username:password@url/database'
    engine = sa.create_engine(conn_string)
    conn = engine.connect()
    res = conn.execute("select 'Success' as Test").fetchall()
    print(res)

Integrating with the IPython/Jupyter SQL Magic
-----------------------------------------------

.. code-block:: python

    %load_ext sql
    %config SqlMagic.autocommit=False
    %config SqlMagic.displaycon=False
    %config SqlMagic.autopandas=True
    %env DATABASE_URL sqream_blue://sqream:sqream@product.isqream.com/master
    %sql select 'Success' as Test
