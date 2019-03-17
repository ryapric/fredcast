import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name = 'fredcast',
    version = '0.1.0',
    author = ['Ryan Price'],
    author_email = ['ryapric@gmail.com'],
    description = 'Short description',
    long_description = long_description,
    url = 'https://url_to_repo',
    packages = setuptools.find_packages(),
    python_requires = '>= 3.6.*',
    install_requires = [
        'flask >= 1.0.2',
        'pandas >= 0.23.4',
        'requests >= 2.21.0',
        # Even though statsmodels depends on scipy, it won't install it?!
        'scipy >= 1.1.0',
        'sqlalchemy >= 1.2.17',
        'statsmodels >= 0.9.0',
        'waitress >= 1.2.0'
    ],
    classifiers = [
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    entry_points = {
        'console_scripts': [
            'fcast-listen = fredcast.flask_app.app:main'
        ]
    },
    include_package_data = True
)
