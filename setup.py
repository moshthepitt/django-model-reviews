"""Setup.py for django-model-reviews."""
import os
import sys

from setuptools import find_packages, setup

import model_reviews as reviews

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

if sys.argv[-1] == "publish":
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("rm -rf build/ *.egg-info/")
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/* --skip-existing")
    print("You probably want to also tag the version now:")
    print(f"  git tag -a v{reviews.__version__} -m 'version {reviews.__version__}'")
    print("  git push --tags")
    sys.exit()

setup(
    name="django-model-reviews",
    version=reviews.__version__,
    description="Easy moderation of changes made to Django models",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Kelvin Jayanoris",
    author_email="kelvin@jayanoris.com",
    url="https://github.com/moshthepitt/django-model-reviews",
    packages=find_packages(exclude=["docs", "*.egg-info", "build", "tests.*", "tests"]),
    install_requires=["Django >=2.2", "django-braces", "django-contrib-comments"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
    ],
    include_package_data=True,
)
