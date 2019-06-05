from setuptools import setup

setup(
    name = 'spaghettini',
    packages = ['spaghettini'],
    version = '0.0.6',
    description = 'A config manager that encourage people not to write spaghetti code',
    author='Qiyang Li',
    author_email='colin.qiyang.li@gmail.com',
    url='https://github.com/ColinQiyangLi/spaghetti',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: GIS'
    ],
    install_requires=["oyaml"],
)
