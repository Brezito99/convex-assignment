from setuptools import setup

setup(
    name='fsa',
    version='0.0.1',
    description='Infinityworks tech test skeleton',
    install_requires=[
        'flask>=2.3.2',
        'requests>=2.31.0',
        'pandas>=2.0.1',
        'PyYaml>=6.0',
        'python-dotenv>=1.0.0'
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
)
