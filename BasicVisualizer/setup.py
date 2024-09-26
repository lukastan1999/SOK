from setuptools import setup, find_packages

setup(
    name="BasicVisualizer",
    version="1.0",
    packages=find_packages(),
    install_requires=['core>=1.0'],
    entry_points = {
        'view_load':
            ['view= BasicVisualizer.BasicVisualizer:BasicVisualizer'],
    },
    zip_safe=True
)
