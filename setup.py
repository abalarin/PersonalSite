from setuptools import setup

setup(
    name='austin',
    packages=['austin'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-security',
        'psycopg2',
        'configparser',
        'requests',
        'urllib',
    ]
)
