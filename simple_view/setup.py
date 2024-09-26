from setuptools import setup, find_packages

setup(
    name="simple-view",
    version="0.1",
    packages=find_packages(),
    install_requires=['core>=0.1'],
    entry_points = {
        'view_load':
            ['view= simple_view.simpleView:SimpleView'],
    },
    zip_safe=True
)