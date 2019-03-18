import setuptools
import importlib

# Avoid native import statements as we don't want to depend on the package being created yet.
def load_module(module_name, full_path):
    spec = importlib.util.spec_from_file_location(module_name, full_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
version = load_module("autoleague.version", "autoleague/version.py")
paths = load_module("autoleague.paths", "autoleague/paths.py")

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()


setuptools.setup(
    name='autoleague',
    packages=setuptools.find_packages(),
    install_requires=[
        'rlbot',
        'rlbottraining>=0.3.0',
        'docopt',
        'trueskill',
        'numpy',
        'pywinauto',
        'pypiwin32',
        'requests',
    ],
    python_requires='>=3.7.0',
    version=version.__version__,
    description='An automatic league-runner for Rocket League bots.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='DomNomNom and the RLBot Community',
    author_email='rlbotofficial@gmail.com',
    url='https://github.com/DomNomNom/AutoLeague',
    keywords=['rocket-league', 'training', 'train'],
    license='MIT License',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
        # Allow people to run `autoleague` instead of `python -m autoleague`
        'console_scripts': ['autoleague = autoleague.__main__:main']
    },
    package_data={
        'autoleague': [
            'autoleague/default_match_config.cfg',
            'autoleague/website/additional_website_code/*',
        ]
    },
)
