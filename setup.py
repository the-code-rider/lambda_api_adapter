from setuptools import setup, find_packages

setup(
    name="lambda_api_adapter",
    version="0.0.1",
    packages=find_packages(),
    author='Lucky Singh',
    author_email='thecoderider42@gmail.com',
    url='https://github.com/the-code-rider/lambda_api_adapter',
    license='MIT',
    description="Convert AWS Lambda handlers to FastAPI endpoints for local testing using a decorator",
    python_requires=">=3.6"
)
