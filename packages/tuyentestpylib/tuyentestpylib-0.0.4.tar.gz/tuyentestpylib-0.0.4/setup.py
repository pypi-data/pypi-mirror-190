from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='tuyentestpylib',
  version='0.0.4',
  description='Test upload python lib',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Nhat Tuyen',
  author_email='nhattuyen0414@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='keyword_npf', 
  packages=find_packages(),
  install_requires=['numpy'] 
)