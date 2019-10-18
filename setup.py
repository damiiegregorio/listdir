from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='listdir',
      version='0.1',
      description='The funniest joke in the world',
      url='https://github.com/damiiegregorio/listdir/tree/packaging',
      author='damiiegregorio',
      author_email='damiiekeith@gmail.com',
      license='MIT',
      packages=['listdir'],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Topic System :: Archiving :: Compression',
        'Operating System :: Microsoft :: Windows',
        'Development Status :: 3 - Alpha'
      ],
      keywords='Hashes',
      include_package_data=True,
      test_suite='nose.collector',
      tests_require=['nose'],
      entry_points={
          'console_scripts': ['listdir=listdir.with_date:main'],
      },
      # install_requires=[
      #     'os',
      # ],
      zip_safe=False)