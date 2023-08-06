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
  version='0.0.2',
  description='A basic and useful tokenizer.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='UesleiDev',
  author_email='uesleibros@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['tokenizer',' token', 'basic-tokenizer', 'basic', 'easy-and-useful'], 
  packages=find_packages(),
  install_requires=['unidecode'] 
)