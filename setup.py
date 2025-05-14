from setuptools import setup, find_packages

setup(
    name="voice-assistant",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'SpeechRecognition',
        'pyaudio',
        'pyttsx3',
    ],
    author="Vineet Singh",
    author_email="vsingh@knox.edu",
    description="A voice-activated AI assistant for PC",
    python_requires='>=3.6',
)