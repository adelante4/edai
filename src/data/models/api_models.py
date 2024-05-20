import pandas as pd
from pydantic import BaseModel, Field


class RequestAPIObject(BaseModel):
    df: pd.DataFrame = Field(description="The input dataframe")
    data_desc: str = Field(description="The description of the dataset")
    column_desc: dict = Field(description="The description of the columns")
    groq_model_name: str = Field(description="The name of the model to be used", default="llama3-70b-8192")
    groq_api_key: str = Field(description="The API key for the Groq model")

    class Config:
        arbitrary_types_allowed = True
