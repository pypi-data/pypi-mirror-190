from setuptools import setup, find_packages

v = {}
with open('airflow_kaldea/__version__.py') as f:
    exec(f.read(), v)

setup(
    name='airflow_kaldea',
    version=v['__version__'],
    url='https://github.com/cloa-io/airflow-kaldea',
    install_requires=['apache-airflow >= 1.10.3'],
    author='Kaldea',
    author_email='support@kaldea.com',
    description='Apache Airflow integration for Kaldea',
    packages=find_packages(exclude=['']),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
