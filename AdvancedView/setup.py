from setuptools import setup, find_packages

setup(
    name="AdvancedView",
    version="1.0",
    packages=find_packages(),
    install_requires=['core>=1.0'],
    entry_points = {
        'view_load':
            ['view=AdvancedView.AdvancedView:AdvancedView'],
    },
    zip_safe=True
)
