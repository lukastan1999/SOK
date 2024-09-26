from setuptools import setup, find_packages

setup(
    name="complex-view",
    version="0.1",
    packages=find_packages(),
    install_requires=['core>=0.1'],
    entry_points = {
        'view_load':
            ['view=complex_view.complex_view:ComplexView'],
    },
    zip_safe=True
)