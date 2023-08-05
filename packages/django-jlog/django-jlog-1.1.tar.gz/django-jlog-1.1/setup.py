import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='django-jlog',
    version='1.1',
    packages=['jlog'],
    long_description_content_type='text/x-rst',
    description="""Log your request and response data""",
    long_description=README,
    author='Javid Aliyev',
    author_email='jaliyev1987@gmail.com',
    url='https://github.com/javiddo/django-jlog',
    license='MIT',
    install_requires=[
        'Django>=1.8',
    ]
)