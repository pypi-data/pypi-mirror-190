from setuptools import setup

setup(
    name='SpeechRecognitionCover',
    packages=['SpeechRecognitionCover'],
    version='1.0.1',
    author='Luka',
    author_email='app6onpython@gmail.com',
    description='Easy cover over SpeechRecognition',
    keywords=['SpeechRecognitionCover', 'Speech recognition cover'],
    install_requires=['SpeechRecognition'],
    classifiers=[
        'Programming Language :: Python :: 3.9'
    ]
)


# python setup.py sdist
# twine upload --skip-existing dist/*