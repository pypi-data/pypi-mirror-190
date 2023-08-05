from setuptools import setup

# with open("README", 'r') as f:
#     long_description = f.read()

setup(
   name='sunnyday_api_weather',
   version='2.3.2',
    packages=['sunnyday_api_weather'],  #same as name
   description='Weather forecast data',
   license="MIT",
   author='Man Creator',
   author_email='example@foo.example',
   keywords =['weather', 'forecast', 'openweather'],
   url="http://www.example/",
   install_requires=['requests'], #external packages as dependencies
   classifiers=[
          'Development Status :: 1 - Planning',
          'Environment :: Console',
          'License :: OSI Approved :: Apache Software License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ]
)
