from setuptools import setup, find_packages

# attention. you need to update the numbers ALSO in the imgstore/__init__.py file
version = "2.0.0"

PACKAGE_NAME = "sleep_models"
with open(f"{PACKAGE_NAME}/_version.py", "w") as fh:
    fh.write(f"__version__ = '{version}'\n")

# This call to setup() does all the work
setup(
    name=PACKAGE_NAME,
    version=version,
    description="Models to learn the mapping between the transcriptome of cells and their sleep/wake state",
    url="https://github.com/shaliulab/sleep-models",
    author="Antonio Ortega",
    author_email="ntoniohu@gmail.com",
    license="MIT",
    classifiers=[
       "License :: OSI Approved :: MIT License",
       "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    install_requires=[
        "anndata==0.7.5",
        "scanpy==1.6.0",
        "numpy==1.21.5",
        "umap-learn==0.5.0",
        "scipy==1.7.3",
        "scikit-learn==1.0.2",
        "interpret==0.2.7",
        "pandas",
        "matplotlib",
        "seaborn",
        "joblib",
        "opencv-python",
        "Pillow",
        "openpyxl",
        "pyaml",
        "seaborn",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "make-dataset=sleep_models.bin.make_dataset:main",
            "train-model=sleep_models.bin.train_model:main",
            "predict=sleep_models.bin.predict:main",
            "make-matrixplot=sleep_models.bin.make_matrixplot:main",
            "make-umapplot=sleep_models.bin.make_umapplot:main",
            "get-marker-genes=sleep_models.bin.get_marker_genes:main",
            "remove-marker-genes=sleep_models.bin.remove_marker_genes:main",
            "sleep-models-sweep=sleep_models.bin.sweep:main",
            "train-torch-model=sleep_models.bin.train_torch_model:main",
            "test-torch-model=sleep_models.bin.test_torch_model:main",
        ]
    },
    python_requires='>=3.7.4',
)
