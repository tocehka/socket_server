from setuptools import setup, find_packages

setup(
    name="socket_server",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    url="https://github.com/tocehka/socket_server",
    author="tocehka",
    install_requires=[
        "flask-socketio>=4.3.0",
        "flask>=1.1.2",
        "python-dotenv>=0.13.0"
    ]
)
