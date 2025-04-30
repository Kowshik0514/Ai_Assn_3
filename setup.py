from setuptools import setup, find_packages

setup(
    name="chess_ai",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'setuptools>=68.0.0',
        'wheel>=0.40.0',
        'python-chess>=1.999',
        'numpy>=1.22.0'
    ],
    python_requires='>=3.8',
    author="Your Name",
    author_email="your.email@example.com",
    description="Chess AI implementation with Minimax and Alpha-Beta pruning",
    keywords="chess, ai, minimax, alpha-beta pruning",
) 