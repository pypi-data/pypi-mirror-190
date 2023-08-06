from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
    name='create_case_folder',
    version='0.0.1',
    description='Create case folder',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='jaytrairat',
    author_email='jaytrairat@outlook.com',
    url='https://github.com/jaytrairat/python-create-case-folder',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'create_case_folder = create_case_folder.main:main'
        ]
    }
)
