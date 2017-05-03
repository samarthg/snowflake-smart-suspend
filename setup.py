from setuptools import setup

setup(name='snowflake-smart-suspend',
      version='0.1.1',
      description='Unix service to suspend the snowflake warehouses smartly to cut the cost.',
      long_description=open('README.md').read(),
      url='https://github.com/samarthg/snowflake-smart-suspend',
      download_url = 'https://github.com/samarthg/snowflake-smart-suspend/archive/v0.1.1.tar.gz',
      author='Samarth Gahire',
      author_email='samarth.gahire@gmail.com',
      license='MIT',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Programming Language :: Python :: 3'
      ],
      packages=['smart_suspend', 'snowflake_config', 'daemonize'],
      install_requires=[
          'pyasn1',
          'snowflake-connector-python',
          'bumpversion',
          'fabric3',
      ],
      entry_points={
          'console_scripts': [
              'smart-suspend = smart_suspend.commandline:run_smart_suspend'
          ]
      },
      zip_safe=False,
      keywords = ['snowflake', 'warehouse', 'optimization', 'cost'],
)