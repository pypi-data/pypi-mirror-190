from setuptools import setup


setup_params = dict(
    
    name =             'pysqream_blue_sqlalchemy',
    version =          '0.1',
    description =      'SQLAlchemy dialect for SQream Blue', 
    long_description = open("README.rst", "r", encoding="utf-8").read(),
    url=               "https://github.com/SQream/pysqream_blue_sqlalchemy",
    
    author =           'SQream',
    author_email =     'info@sqream.com',
    
    classifiers =      [
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    keywords = 'database sqlalchemy sqream sqreamdb',

    python_requires =  '>=3.7',
    
    install_requires = ['sqlalchemy>=1.3.18',
                        'pysqream-blue>=1.0.22',
                        'setuptools==57.4.0',
                        'pytest==6.2.3',
                        'pudb==2022.1.2',
                        'pandas==1.1.5',
                        'numpy==1.20',
                        'alembic==1.5.8'],
    
    packages         = ['pysqream_blue_sqlalchemy'], 
    
    entry_points =     {'sqlalchemy.dialects': 
        ['sqream_blue = pysqream_blue_sqlalchemy.dialect:SqreamBlueDialect']
    },
    # sqream://sqream:sqream@localhost/master
)


if __name__ == '__main__':
    setup(**setup_params)
