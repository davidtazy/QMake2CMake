from setuptools import setup




setup(name='QMakeToCMake',
      version='0.1',
      description='help to convert qmake .pro files in CMakeLists.txt',
      classifiers=[
        'Development Status :: 4 - Beta'],
      keywords='qmake Qt5 modern cmake CMakeLists.txt converter',
      url='http://github.com/davidtazy/QMakeToCMake',
      author='David Allemant',
      author_email='notmymail@example.com',
      license='MIT',
      packages=['q2c'],
      entry_points = {
        'console_scripts': ['q2c=q2c.command_line:main'],
      },
      install_requires=[
          'semver',
      ],
      test_suite="tests",
      zip_safe=False)
