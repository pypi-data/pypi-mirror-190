from setuptools import setup

setup(
    name='jupyter_database_connector',
    version='0.1.0',
    packages=['jupyter_database_connector'],
    include_package_data=True,
    install_requires=[
        'sqlalchemy',
        'jupyter_server'
    ]
)