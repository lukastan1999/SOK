from setuptools import setup, find_packages

setup(
    name="core",
    version="0.1",
    packages=find_packages(),
    # requiring Django later than 2.1
    install_requires=['Django>=2.1', 'python-dateutil>=2.8.0'],

    package_data={'core': ['static/*.css', 'static/*.js', 'static/*.html','templates/*.html']},
    zip_safe=False
)
