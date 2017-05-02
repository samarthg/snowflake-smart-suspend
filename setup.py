from setuptools import setup

setup(name='snowflake_smart_suspend',
      version='0.0.0',
      description='Unix service to suspend the snowflake warehouses smartly to cut the cost.',
      long_description=open('README.md').read(),
      url='https://github.com/samarthg/snowflake-smart-suspend',
      download_url = 'https://github.com/samarthg/snowflake-smart-suspend/archive/v0.0.0.tar.gz'
      author_email='samarth.gahire@gmail.com',
      license='MIT',
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
