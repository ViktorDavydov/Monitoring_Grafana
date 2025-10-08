"""Setup script for the demo application."""

from setuptools import setup, find_packages

setup(
    name="monitoring-demoapp",
    version="1.0.0",
    description="Demo application for Grafana monitoring with Prometheus metrics (pure Python)",
    author="Demo App",
    python_requires=">=3.8",
    packages=find_packages(),
    install_requires=[
        "prometheus-client>=0.17.0",
    ],
    entry_points={
        "console_scripts": [
            "demoapp-server=cmd.app.main:main",
            "demoapp-load=cmd.load.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Monitoring",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
    ],
)



