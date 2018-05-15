from setuptools import setup

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='scikit-hyper',

    version='0.0.2c',

    packages=['skhyper',
              'skhyper.view',
              'skhyper.view._form',
              'skhyper.naive_bayes',
              'skhyper.svm',
              'skhyper.cluster',
              'skhyper.process',
              'skhyper.decomposition'],

    python_requires='>=3.5.0',

    url='https://github.com/priyankshah7/scikit-hyper',

    download_url='https://github.com/priyankshah7/scikit-hyper/archive/v0.0.2.tar.gz',

    license='BSD 3-Clause',

    author='Priyank Shah',

    author_email='priyank.shah@kcl.ac.uk',

    description='Hyperspectral data analysis and machine learning',

    long_description=LONG_DESCRIPTION,

    long_description_content_type='text/markdown',

    keywords=['hyperspectral',
              'data-analysis',
              'clustering',
              'matrix-decompositions',
              'hyperspectral-analysis',
              'machine learning'],

    install_requires=['numpy',
                      'scipy',
                      'matplotlib',
                      'pyqt5',
                      'pyqtgraph',
                      'scikit-learn']
)
