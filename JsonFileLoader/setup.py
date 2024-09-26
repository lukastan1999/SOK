from setuptools import setup, find_packages

setup(
    name="JsonFileLoader",
    version="1.0",
    packages=find_packages(),
    install_requires=['core>=1.0', 'python-dateutil>=2.9.0'],
    entry_points={
        'data_load':
            ['loader_json=JsonFileLoader.JsonFileLoader:JsonFileLoader'],
    },
    zip_safe=True
)
