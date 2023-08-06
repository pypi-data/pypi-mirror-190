from setuptools import setup, find_packages


setup(
    name='collibra_luigi_client',
    version='0.1.13',
    description="Collibra Luigi client with simple 3 tasks for importing assets",
    license='MIT',
    author="collibra",
    author_email='antonio.castelo@collibra.com',
    #packages=find_packages(exclude=["logs", "output", "stage"]),
    packages=find_packages('.'),
    package_dir={'': '.'},
    url='',
    keywords=["collibra", "luigi"],
    install_requires=['collibra_core==2.0.0.post7', 'collibra_importer==2.0.0.post6', 'cryptography==38.0.1', 'luigi==3.2.0', 'python-dotenv==0.20.0', 'toml==0.10.2', 'requests==2.27.1', 'apache_beam==2.42.0']
)
