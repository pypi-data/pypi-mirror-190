import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

     name="UIBotPy",
     version='0.0.1',
     author="Valdemar Petersen",
     author_email="valdemarlpt@gmail.com",
     description="UI Automation",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/you/your_package_repo",
     packages=['UIBotPy'],
     classifiers=[
         "Programming Language :: Python :: 3.7",
         "Operating System :: OS Independent",
     ],
 )
