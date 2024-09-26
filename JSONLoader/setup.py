from setuptools import setup, find_packages

setup(
    name="jsonLoader",
    version="1.0",
    packages=find_packages(),
    install_requires=['core>=1.0', 'python-dateutil>=2.9.0'],
    entry_points={
        'data_load':
            ['loader_json=loader_json.loaderJSON:JsonLoader'],
    },
    data_files=[('test_data', ['loader_json/test_data/primer1.json',
                               'loader_json/test_data/primer2.json',
                               'loader_json/test_data/primer3.json'])],
    zip_safe=True
)
