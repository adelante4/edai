import logging

import pandas as pd
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.experimental import PandasQueryEngine

from src.data.models.api_models import RequestAPIObject
from src.data.models.response_models import PreprocessingOutput, FeatureEngOutput, VisualizationOutput, QuestionsOutput, \
    PythonCodeOutput, Code
from src.data.notebook import Notebook
from src.data.utils import dataframe_info
from src.edai.prompts import preprocess_template, feature_eng_template, visualization_template, questions_template, \
    qa_template
from llama_index.core import Settings
from llama_index.llms.groq import Groq


class Edai:
    def __init__(self, request_data: RequestAPIObject):
        self.request_data = request_data
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.info("Edai instance created")

        self.query_engine = PandasQueryEngine(df=request_data.df, verbose=False)

        self.nb = Notebook("data.csv")

    def eda(self):
        self.logger.info("Starting EDA...")
        preprocessing_steps = self.preprocess_data()

        self.feature_engineering(preprocessing_steps)
        self.visualize_data()
        self.qa()
        self.nb.save("edai_notebook.ipynb")
        self.logger.info("EDA complete")

    def preprocess_data(self):
        self.logger.info("Preprocessing data...")
        preprocessing_program = self.get_completion_program(
            output_parser=PydanticOutputParser(PreprocessingOutput),
            prompt_template_str=preprocess_template.get_template(),
            output_cls=PreprocessingOutput,
        )
        preprocessing_steps = preprocessing_program(dataset_info=dataframe_info(self.request_data.df,
                                                                                self.request_data.data_desc,
                                                                                self.request_data.column_desc))

        preprocessing_codes = preprocessing_steps.generate_code(self.query_engine)

        self.nb.add_cell(f"## Preprocessing Steps", cell_type="markdown")
        self.request_data.df = self.nb.add_generated_code(preprocessing_codes, self.request_data.df)

        self.logger.info("Data preprocessing complete")
        return preprocessing_steps

    def feature_engineering(self, preprocessing_steps):
        self.logger.info("Feature engineering...")

        feature_eng_program = self.get_completion_program(
            output_parser=PydanticOutputParser(FeatureEngOutput),
            prompt_template_str=feature_eng_template.get_template(),
            output_cls=FeatureEngOutput,
        )
        feature_eng_steps = feature_eng_program(dataset_info=dataframe_info(self.request_data.df,
                                                                            self.request_data.data_desc,
                                                                            self.request_data.column_desc),
                                                preprocessing_steps="\n".join(
                                                    "- " + step for step in preprocessing_steps.steps))

        feature_eng_codes = feature_eng_steps.generate_code(self.query_engine)
        self.nb.add_cell(f"## Feature Engineering Steps", cell_type="markdown")
        self.request_data.df = self.nb.add_generated_code(feature_eng_codes, self.request_data.df)
        self.logger.info("Feature engineering complete")

    def visualize_data(self):
        self.logger.info("Visualizing data...")
        visualization_program = self.get_completion_program(
            output_parser=PydanticOutputParser(VisualizationOutput),
            prompt_template_str=visualization_template.get_template(),
            output_cls=VisualizationOutput,
        )

        visualizations = visualization_program(dataset_info=dataframe_info(self.request_data.df,
                                                                           self.request_data.data_desc,
                                                                           self.request_data.column_desc))
        visualization_codes = visualizations.generate_code(self.query_engine)
        self.nb.add_cell(f"## Data visualization", cell_type="markdown")
        self.request_data.df = self.nb.add_generated_code(visualization_codes, self.request_data.df)
        self.logger.info("Data visualization complete")

    def qa(self):
        self.logger.info("Questions and answers...")
        questions_program = self.get_completion_program(
            output_parser=PydanticOutputParser(QuestionsOutput),
            prompt_template_str=questions_template.get_template(),
            output_cls=QuestionsOutput,
        )

        qa_program = self.get_completion_program(
            output_parser=PythonCodeOutput(),
            prompt_template_str=qa_template.get_template(),
            output_cls=Code,
        )
        dataset_info = dataframe_info(self.request_data.df,
                                      self.request_data.data_desc,
                                      self.request_data.column_desc)
        questions = questions_program(dataset_info=dataset_info)

        question_codes = questions.generate_code(qa_program, dataset_info)
        self.nb.add_cell(f"## Questions to Answer", cell_type="markdown")
        self.request_data.df = self.nb.add_generated_code(question_codes, self.request_data.df)
        self.logger.info("Questions and answers complete")

    @staticmethod
    def get_completion_program(output_parser, prompt_template_str, output_cls):
        return LLMTextCompletionProgram.from_defaults(
            output_parser=output_parser,
            output_cls=output_cls,
            prompt_template_str=prompt_template_str,
            verbose=False,
        )
