"""
Setup script for Project Prometheus
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

setup(
    name='project-prometheus',
    version='1.0.0',
    description='Enterprise-Grade AI Detection System for Academic Integrity',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='Project Prometheus Team',
    author_email='contact@projectprometheus.ai',
    url='https://github.com/yourusername/project-prometheus',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'fastapi>=0.104.1',
        'uvicorn[standard]>=0.24.0',
        'python-multipart>=0.0.6',
        'opencv-python>=4.8.1.78',
        'numpy>=1.24.3',
        'Pillow>=10.1.0',
        'scipy>=1.11.4',
        'scikit-learn>=1.3.2',
        'pandas>=2.1.3',
        'openpyxl>=3.1.2',
        'pydantic>=2.5.0',
        'pydantic-settings>=2.1.0',
        'python-dotenv>=1.0.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.3',
            'pytest-asyncio>=0.21.1',
            'black>=23.11.0',
            'flake8>=6.1.0',
        ],
        'google': [
            'google-api-python-client>=2.108.0',
            'google-auth>=2.23.4',
            'google-auth-oauthlib>=1.1.0',
        ],
        'microsoft': [
            'msal>=1.23.0',
            'requests>=2.31.0',
        ],
        'face': [
            'dlib>=19.24.2',
            'retina-face>=0.0.13',
            'deepface>=0.0.79',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Education',
    ],
    entry_points={
        'console_scripts': [
            'prometheus=backend.api.main:main',
        ],
    },
)
