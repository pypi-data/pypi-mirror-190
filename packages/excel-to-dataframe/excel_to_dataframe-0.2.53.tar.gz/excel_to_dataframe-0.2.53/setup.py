import setuptools    

setuptools.setup(
    name='excel_to_dataframe',
    version='0.2.53',
    author='Nelson Rossi Bittencourt',
    author_email='nbittencourt@hotmail.com',
    description='Excel to Pandas or Microsoft Dataframe',
    long_description='C++ dll to converts Excel worksheets to Pandas or Microsoft dataframes',
    long_description_content_type="text/markdown",
    url='https://github.com/nelsonbittencourt/excel_to_dataframe',
    license='MIT',
    packages=['excel_to_dataframe'],
	include_package_data=True,
	package_data={'':['excel_to_df.dll']},
    install_requires=['pandas','openpyxl'],
    classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: End Users/Desktop',
    
    # Pick your license as you wish (should match "license" above)
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    
    # OS
    'Operating System :: Microsoft :: Windows'
],
)