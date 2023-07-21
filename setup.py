from setuptools import setup

setup(
   name='apkpatcher',
   version='1.0.0',
   description='Automate the task of patching an apk with frida-gadget. fork of badadaf/apkpatcher',
   author='Marcel Alexandru Nitan',
   author_email='nitan.marcel@gmail.com',
   url='https://github.com/nitanmarcel/apkpatcher',
   scripts=['apkpatcher'],
   install_requires=[
       'requests',
       'appdirs',
   ],
)