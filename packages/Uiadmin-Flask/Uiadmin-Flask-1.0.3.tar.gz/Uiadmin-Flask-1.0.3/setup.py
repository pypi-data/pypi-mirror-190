"""
Uiadmin-Flask
-------------
 
an flask version for uiadmin
"""
from setuptools import setup,find_packages
 
setup(
    name='Uiadmin-Flask',
    version='1.0.3',
    url='http://uiadmin.net',
    license='Apache2',
    author='jry',
    author_email='ijry@qq.com',
    description='uiadmin的python实现',
    long_description=__doc__,
    packages=find_packages(), # 使用find_packages才会发布插件下的子目录
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
