from setuptools import setup, find_packages

setup(
    name="jsonLoader",
    version="0.1",
    packages=find_packages(),
    install_requires=['core>=0.1', 'python-dateutil>=2.8.0'],
    entry_points={
        'data_load':
            ['loader_json=loader_json.loaderJSON:JsonLoader'],
    },
    data_files=[('test_data', ['loader_json/test_data/drzaveManji.json',
                               'loader_json/test_data/drzave.json',
                               'loader_json/test_data/example1.json',
                               'loader_json/test_data/example2.json',
                               'loader_json/test_data/example3.json',
                               'loader_json/test_data/example5.json',
                               'loader_json/test_data/example6.json'])],
    zip_safe=True
)