from setuptools import setup, find_packages

setup(
    name="core",
    version="1.0",
    packages=find_packages(),
    install_requires=['Django>=4.0', 'python-dateutil>=2.9.0'],
    package_data={'core': ['static/*.css', 'static/*.js', 'static/*.html','templates/*.html']},
    zip_safe=False
)
