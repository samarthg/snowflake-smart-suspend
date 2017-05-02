from setuptools import setup

setup(name='snowflake_smart_suspend',
      version='0.1.0',
      description='To suspend running and unused warehouse intelligently',
      url='',
      author='Samarth Gahire',
      author_email='samarth.gahire@gmail.com',
      license='MIT',
      packages=['smart_suspend', 'snowflake_config', 'daemonize'],
      install_requires=[
          'pyasn1',
          'snowflake-connector-python',
      ],
      entry_points={
          'console_scripts': [
              'smart-suspend = smart_suspend.commandline:run_smart_suspend'
          ]
      },
      zip_safe=False)
