from setuptools import setup, find_packages

setup(
    name='Floom',  # Floom Python SDK
    version='1.0.2',
    packages=find_packages(exclude=['examples*']),  # Excluding examples directories
    install_requires=[
        # No third-party packages
    ],
    author='FloomAI',
    author_email='dev@floom.ai',
    description='Floom orchestrates & executes Generative AI pipelines, Empowering Developers and DevOps to focus on '
                'what matters.',
    url='https://github.com/FloomAI/FloomSDK-Python',
)
