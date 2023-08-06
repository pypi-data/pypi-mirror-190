from setuptools import setup, find_packages

setup(
    name="collect-framework-test",
    version="1.1.1",
    author="Drakosha295",
    description="Simple collect framework",
    packages=find_packages("src"),
    package_dir={"": "src"},
	install_requires=[
        "pytest"
    ],
	entry_points={"console_scripts": ["collect_framework_test = src.__main__:main"]},
	test_suite="tests",
	include_package_data=True
)