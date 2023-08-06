# LLMs that are Helpful, Honest, Harmless, and Huggy 🤗

## Installation

Download and install `h4` by running:

```bash
python -m pip install h4
```

If you want the bleeding-edge version, install from source by running:

```bash
python -m pip install git+https://github.com/huggingface/h4.git
```

### Developer installation

To contribute code to this project, first create a Python virtual environment using e.g. Conda:

```bash
conda create -n h4 python=3.8 && conda activate h4
```

Then install the base requirements with:

```bash
python -m pip install -e '.[dev]'
```

This will install core packages like `black` and `isort` that we use to ensure consistent code formatting.

## Formatting your code

We use `black` and `isort` to ensure consistent code formatting. After following the installation steps, you can check your code locally by running:

```
make style && make quality
```