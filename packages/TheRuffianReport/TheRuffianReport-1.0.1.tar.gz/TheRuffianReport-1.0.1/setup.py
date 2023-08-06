from distutils.core import setup
from setuptools import find_packages

with open("README.md", 'rb') as f:
    long_description = f.read()

setup(name='TheRuffianReport',  # 你包的名称
      version='1.0.1',  # 版本号
      description='test',  # 描述
      long_description=long_description,  # 长描述
      long_description_content_type='text/markdown',
      author='TheRuffian',
      author_email='bugpz2779@gmail.com',
      url='https://github.com/the-ruffian/TheRuffianReport',
      download_url='https://codeload.github.com/the-ruffian/TheRuffianReport/zip/refs/heads/master',
      install_requires=['requests'],  # 依赖第三方库
      license='MIT License',
      keywords=[ 'the-ruffian', 'ruffianTest', 'ruffian','TheRuffian', 'TheRuffianReport'],
      packages=find_packages(),
      platforms=['all'],  # 平台
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Testing',
          'Development Status :: 5 - Production/Stable'
      ],
      )
