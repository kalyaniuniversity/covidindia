import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="covdata",
    version="1.2.0",
    author="Dripta senapati",
    author_email="driptasenapati97@gmail.com",
    description="A package that can grab all data of Covid-19 cases in India",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kalyaniuniversity/covidindia",
    packages=setuptools.find_packages(exclude=[]),
    include_package_data=True,
        package_data={
            'SERVER/templates': [
                'SERVER/templates/index_demo.html',
                'SERVER/templates/index_analysis.html',
                'SERVER/templates/index_home.html',
                'SERVER/templates/index_rank.html',
                'SERVER/templates/index_state.html',
                'SERVER/templates/index_dashboard.html'
            ],
            'SERVER/static': [
                'SERVER/static/demo.js',
                'SERVER/static/analysis.js',
                'SERVER/static/main.js',
                'SERVER/static/rank.js',
                'SERVER/static/state.js',
                'SERVER/static/jquery.nice-select-analysis.js',
                'SERVER/static/jquery.nice-select-demo.js',
                'SERVER/static/jquery.nice-select-home.min.js',
                'SERVER/static/jquery.nice-select-rank.js',
                'SERVER/static/jquery.nice-select-state.js',
                'SERVER/static/style.css',
                'SERVER/static/style_demo.css',
                'SERVER/static/style_analysis.css',
                'SERVER/static/style_rank.css',
                'SERVER/static/style_state.css',
                'SERVER/static/nice-select-analysis.css',
                'SERVER/static/nice-select-demo.css',
                'SERVER/static/nice-select-home.css',
                'SERVER/static/nice-select-rank.css',
                'SERVER/static/nice-select-state.css'
            ],
    },
    install_requires=[
        'pandas>=1.0.0',
        'numpy>=1.18.1',
        'matplotlib>=3.1.3',
        'datetime',
        'flask>=1.1.1',
        'Flask-CacheBuster>=1.0.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "covdata=covdata.cli:main",
        ]
    },
    python_requires='>=3.6',
)
