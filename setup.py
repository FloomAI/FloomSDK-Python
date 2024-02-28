from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='Floom',  # Floom Python SDK
    version='1.0.3',
    packages=find_packages(exclude=['examples*']),  # Excluding examples directories
    install_requires=requirements,
    include_package_data=True,
    author='FloomAI',
    author_email='dev@floom.ai',
    description='Floom orchestrates & executes Generative AI pipelines, Empowering Developers and DevOps to focus on '
                'what matters.',
    python_requires='>=3.0',
    url='https://github.com/FloomAI/FloomSDK-Python',
)
