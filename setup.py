from setuptools import setup

setup(
   name='apkpatcher-cli',
   version='1.3.2',
   description='Automate the task of patching an apk with frida-gadget. fork of badadaf/apkpatcher',
   author='Marcel Alexandru Nitan',
   author_email='nitan.marcel@gmail.com',
   url='https://github.com/nitanmarcel/apkpatcher',
   keywords=['FRIDA', 'APK'],
   scripts=['apkpatcher'],
   install_requires=[
       'requests',
       'appdirs'
   ],
   classifiers=[
    'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',

   ]
)
