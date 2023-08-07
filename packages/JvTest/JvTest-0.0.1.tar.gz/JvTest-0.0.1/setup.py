from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='JvTest',
    version='0.0.1',
    license='MIT License',
    author='Jvsm Games',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='jvsm5000wt@gmail.com',
    keywords='teste',
    description=u'Apenas Testando',
    packages=['JvTest'],
    install_requires=['requests'],)