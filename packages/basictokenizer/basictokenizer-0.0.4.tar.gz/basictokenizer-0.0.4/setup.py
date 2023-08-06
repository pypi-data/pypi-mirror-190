from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='basictokenizer',
  version='0.0.4',
  description='A basic and useful tokenizer.',
  long_description='The Tokenizer package provides an easy-to-use and efficient way to tokenize text data. The Tokenizer package is built with performance in mind, making it a fast and reliable choice for tokenizing text data at scale.',
  url='',  
  author='UesleiDev',
  author_email='uesleibros@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['tokenizer',' token', 'basic-tokenizer', 'basic', 'easy-and-useful'], 
  packages=find_packages(),
  install_requires=['unidecode'] 
)