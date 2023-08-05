from setuptools import setup

setup(name="clashroyale-api",
      version="0.0.2",
      description="A Clash Royale API",
      long_description=open('README.rst').read(),
      author="Luca Koch",
      author_email="luca.koch@aon.at",
      url="https://github.com/Acul747/ClashRoyale-API",
      classifiers=["Development Status :: 1 - Planning",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python"],
      license="MIT License",
      keywords=["cr", "clash", "clashroyale"],
      include_package_data=True,
      python_requires='>=3.11',
      install_requires=[
          "requests~=2.28.2"
      ]
)
