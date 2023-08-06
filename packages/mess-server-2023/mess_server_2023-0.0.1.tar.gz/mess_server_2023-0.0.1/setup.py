from setuptools import setup, find_packages

setup(name="mess_server_2023",
      version="0.0.1",
      description="mess_server_proj",
      author="Mihanyga",
      author_email="volk.mixail@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
