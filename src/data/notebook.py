import json

import pandas as pd

from src.data.models.response_models import Code


class Notebook:
    def __init__(self, dataset_name):
        """
        Initialize a new Jupyter notebook structure with a dataset loading cell.

        Parameters:
        dataset_name (str): The name of the dataset to be loaded into a pandas DataFrame.
        """
        self.notebook = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "## Load data"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [
                        "import pandas as pd\n",
                        "import numpy as np\n",
                        f"df = pd.read_csv('{dataset_name}')\n",
                        "df.head()"
                    ]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                },
                "language_info": {
                    "codemirror_mode": {
                        "name": "ipython",
                        "version": 3
                    },
                    "file_extension": ".py",
                    "mimetype": "text/x-python",
                    "name": "python",
                    "nbconvert_exporter": "python",
                    "pygments_lexer": "ipython3",
                    "version": "3.8.5"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }

    def add_cell(self, cell_content, cell_type="code"):
        """
        Add a cell to the notebook.

        Parameters:
        - cell_content: The content of the cell as a string.
        - cell_type: The type of the cell ('code' or 'markdown').
        """
        if cell_type == "code":
            cell = {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [cell_content]
            }
        elif cell_type == "markdown":
            cell = {
                "cell_type": "markdown",
                "metadata": {},
                "source": [cell_content]
            }
        else:
            raise ValueError("Invalid cell type. Must be 'code' or 'markdown'.")

        self.notebook["cells"].append(cell)

    def add_generated_code(self, code: list[Code], df: pd.DataFrame):
        """
        Add generated codes cell to the notebook.

        Parameters:
        - code: The list of code objects to add to the notebook.
        - df: The pandas DataFrame to be used in the code.
        """
        for c in code:
            try:
                df = c.execute(df)
                self.add_cell(f"### {c.title}\n\n{c.description}", "markdown")
                self.add_cell(c.code, "code")
            except Exception as e:
                print(f"Error executing code: {e}")
                # TODO: Add retry logic here

        return df

    def save(self, filename):
        """
        Save the notebook to a file.

        Parameters:
        - filename: The filename for the notebook (should end with .ipynb).
        """
        with open(filename, 'w') as f:
            json.dump(self.notebook, f, indent=2)
