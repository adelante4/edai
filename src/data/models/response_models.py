from abc import ABC
from typing import List, Optional

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field
from llama_index.core.output_parsers import ChainableOutputParser
from llama_index.experimental.query_engine import PandasQueryEngine


class Code(BaseModel):
    title: str = Field(None, title="Title of the code")
    description: str = Field(None, title="Description of the code")
    code: str = Field(None, title="Code to execute")

    def execute(self, df: Optional[pd.DataFrame]):
        local_vars = {'df': df, 'pd': pd, 'np': np}
        exec(self.code, {}, local_vars)
        return local_vars['df']


class InstructionSteps(ABC, BaseModel):

    def generate_code(self, query_engine: PandasQueryEngine) -> List[Code]:
        codes = []
        for step, step_title in zip(self.steps, self.step_titles):
            code = query_engine.query(step)
            codes.append(Code(title=step_title, description=step,
                              code=code.metadata['pandas_instruction_str']))

        return codes


class PreprocessingOutput(InstructionSteps):
    step_titles: List[str] = Field(..., title="Preprocessing Steps Titles")
    steps: List[str] = Field(..., title="Preprocessing Steps Descriptions")


class FeatureEngOutput(InstructionSteps):
    step_titles: List[str] = Field(..., title="Feature Engineering Steps Titles")
    steps: List[str] = Field(..., title="Feature Engineering Steps Descriptions")


class VisualizationOutput(InstructionSteps):
    step_titles: List[str] = Field(..., title="Visualization Steps Titles")
    steps: List[str] = Field(..., title="Visualization Steps Descriptions")


class PythonCodeOutput(ChainableOutputParser):
    """
    Custom code output parser.
    """
    def parse(self, output: str) -> Code:
        output = output.strip()
        title = output.split('Title:')[1].split('Description:')[0].strip()
        description = output.split('Description:')[1].split('```')[0].strip()
        code = output.split('```')[1].strip()
        description += "\n" + output.split('```')[-1].strip()

        return Code(title=title, description=description, code=code)


class QuestionsOutput(BaseModel):
    questions: List[str] = Field(..., title="Questions to be answered from the data")

    def generate_code(self, qa_program, dataset_info) -> List[Code]:
        codes = []
        for question in self.questions:
            answer = qa_program(dataset_info=dataset_info,
                                question=question)

            codes.append(answer)

        return codes
