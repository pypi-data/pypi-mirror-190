from setuptools import setup

setup(
    name='SpeechRecognitionCover',
    version='1.0.0',
    author='Luka',
    license='MIT',
    author_email='app6onpython@gmail.com',
    description='Easy cover for SpeechRecognition library',
    install_requires=[
        'SpeechRecognition',
        'PyAudio'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.9'
    ]
)

# python setup.py sdist
# twine upload --skip-existing dist/*