# Streamlit Application Template
A template for a simple python Streamlit application with data assets and multiple pages.

Customize this template by renaming the package `streamlit_template_pkg`, adding your own data to the `data` folder
and modifying the Streamlit app contents and pages!

# Setup and Installation
## 1. Create a Conda Virtual Environment

Create a new conda environment named `streamlit_template` with Python 3.12:
```bash
conda create -n streamlit_template python=3.12 -y
```

## 2. Activate the environment:
```bash
conda activate streamlit_template
```

## 3. Install the project package and dependencies
The project dependencies alone can be installed by running `pip install -r requirements.txt` or `conda install --file requirements.txt`.

You can install the package and its dependencies by running `pip install .`.

To install the package in editable mode with development and test dependencies `pip install -e ".[dev,test]"`.

## 4. Run the application
Start the Streamlit application by running `app.py` from the project root:
```bash
streamlit run app.py
```
The application will open in your web browser.

# Data
The data included in the `data` folder is the following:
- `data/public_postsecondary_awards_conferred_by_institution_20260125.csv`: This dataset contains the count of certificates and degrees conferred at all public Massachusetts institutions of higher education since 2014. See details about the dataset on [its page at the Massachusetts Education-to-Career Research and Data Hub](https://educationtocareer.data.mass.gov/College-and-Career/Public-Postsecondary-Awards-Degrees-Conferred-by-I/5yjf-27fz/about_data). Data was exported on January 25th, 2025.

# Project Structure
This project follows a clear separation between the **Streamlit application** and the **reusable Python package**:

```
streamlit_template/
├── app.py                          # Main Streamlit application entry point
├── config.py                       # Shared configuration used in the Streamlit application (data paths, constants)
├── pages/                          # Streamlit pages (auto-discovered by Streamlit)
│   ├── degrees_over_time.py       # Page showing awards trends over time
│   └── degrees_by_institution.py  # Page showing awards by institution
├── data/                           # Data files (not part of the installed package)
│   └── *.csv
├── streamlit_template_pkg/         # Python package (installable via pip)
│   ├── __init__.py
│   ├── data_utils.py              # Data loading and manipulation functions
│   └── visualizations.py          # Plotly visualization functions
├── tests/                          # Unit tests for the package
│   └── test_*.py
├── pyproject.toml                  # Package metadata and dependencies
├── requirements.txt                # Runtime dependencies
└── README.md                       # This file
```

## Key Design Decisions

### App Files vs. Package Code
- **App files** (`app.py`, `pages/`, `config.py`): Streamlit-specific code that runs when you execute `streamlit run app.py`. These files are NOT part of the installed package.
- **Package code** (`streamlit_template_pkg/`): Reusable Python functions for data processing and visualization. This code can be imported by the app or used independently in other projects.

### Data Loading
- The path to the CSV data file is defined in `config.py` and shared across all pages
- The `@st.cache_data` decorator ensures the CSV is read only once per session, even though multiple pages call the same function. See more on [caching in the Streamlit documentation](https://docs.streamlit.io/develop/concepts/architecture/caching).
- All pages use the same `CSV_PATH` from `config.py`, ensuring they share the cached data

### Multi-Page Application
Streamlit automatically discovers pages in the `pages/` directory and creates a sidebar navigation. See more details on [multipage apps in the Streamlit documentation](https://docs.streamlit.io/develop/concepts/multipage-apps/overview). Each page:
1. Imports the shared `CSV_PATH` from `config.py`
2. Calls `load_awards_data(CSV_PATH)` to get the cached DataFrame
3. Uses visualization functions from `streamlit_template_pkg.visualizations`
4. Provides interactive controls for exploring the data

# Testing
This project uses [pytest](https://docs.pytest.org/en/stable/) for unit testing. If you have installed the `test` dependencies, you can run the tests with the `pytest` command.

# Linting and Formatting
This project relies on [Ruff](https://docs.astral.sh/ruff/) for formatting code and flagging potential issues. Ruff is installed with the `dev` dependencies set.
- *Linting* is the term for a code analysis tool that can flag potential bugs or programming errors. Ruff's linter is run with the `ruff check` command.
- *Formatting* standardizes code to make it consistent, easier to read, and avoid changes that aren't meaningful (e.g. changes to tabs, whitespace, quotes styles, etc...) during version control and pull requests. Run Ruff's formatter with the `ruff format` command.

# Contributing
These are the recommended development guidelines you should follow when changing the code in this project, to make it easy for others to easily follow and review your code:
- Keep project dependencies up to date by updating requirements.txt or the `dev` and `test` sections in pyproject.toml if you use a new Python package import or remove one.
- Follow the [PEP 8 Style Guide for Python Code](https://peps.python.org/pep-0008/). Regularly checking your code with `ruff format` and `ruff check` and committing files to git will help you do this. You can also set up [VS Code to automatically lint and format code using `ruff`](https://docs.astral.sh/ruff/editors/setup/).
- Use [Google Style Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) for your modules and functions. Try the [autoDocstring VS Code extension](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring) to help you generate Docstrings quickly.

# Acknowledgements
This repository was created by Virginia Partridge for CICS296x: Public Interest Technology Clinic Group Independent Study at the University of Massachusetts, Amherst.

It was created with inspiration from [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/) and [Andy McDonald's Streamlit App Project Structure Guide](https://andymcdonaldgeo.substack.com/p/how-to-structure-and-organise-a-streamlit-app-e66b65ece369). Claude Code was used to prototype the first version of the pages on the Streamlit app and generate unit tests for loading data.