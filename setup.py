from distutils.core import setup

with open("requirements.txt", "r", encoding="utf8") as f:
    dependencies = f.read()

setup(
    name="Hashi SDK",
    version="0.1.0",
    description="A low-level asynchronous SDK for OPQ QQ robots.",
    author="Mix",
    author_email="admin@yami.im",
    url="https://github.com/mixmoe/HashiSDK",
    install_requires=dependencies,
    python_requires=">= 3.8.0",
    packages=["hashi"],
)

