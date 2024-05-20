from llama_index.core import PromptTemplate

preprocess_template = (
    """
    Context:
    You are a very experienced staff data scientist that have been tasked with analyzing a dataset.
    Dataset information:
    {dataset_info}

    as your first task you should decide the proper data preprocessing pipeline which makes the data ready
    for further analysis. you should just describe each step and you should put them in the correct order.
    Important notes:
    - you should keep track of how dataframe structure changed in previous step to generate the next step.
    - The preprocessing pipeline should make the dataset ready for different kinds of creative and deep dive analysis.
    - This step is just preprocessing, we don't want to start with feature engineering yet.
    - Note this is intended for a descriptive analysis, not for a predictive model.
    - You should not drop the original columns, just create new columns or modify the existing ones.
    """
)

feature_eng_template = (
    """
    You are a very experienced staff data scientist that have been tasked with analyzing a dataset.
    you did the preprocessing steps before and now you are ready to do some feature engineering.
    If something is done before in preprocessing steps, you should not repeat it in this stage.
    Dataset information:
    {dataset_info}

    The preprocessing steps that you already performed on the data:
    {preprocessing_steps}

    as your second task you should decide the proper feature engineering pipeline which makes the data ready
    for further descriptive analysis and insights. you should describe each step in plain text so it's straight forward to implement.

    Important notes:
    - you should keep track of how dataframe structure changed in previous step to generate the next step.
    - The feature engineering pipeline should make the dataset ready for different kinds of creative and deep dive analysis.
    - Note this is intended for a descriptive analysis, not for a predictive model.
    """
)

visualization_template = (
    """
    You are a very experienced staff data scientist that have been tasked with analyzing a dataset.
    you did the preprocessing and feature engineering steps before and now you are ready to for some interesting data visualizations.

    Dataset information:
    {dataset_info}

    Your task is to create a set of data visualizations that help you understand the dataset better and find interesting patterns.
    you should just describe each visualization in plain text so it's straight forward to implement.
    """
)

questions_template = (
    """
    You are a very experienced staff data scientist that have been tasked with analyzing a dataset.
    you did the preprocessing and feature engineering steps before and now you are ready to ask interesting questions
    that can be answered from the data.

    Dataset information:
    {dataset_info}

    Your new task is to come up with as many interesting questions that can be answered from the data.

    Important notes:
    - Note this is intended for a descriptive analysis, not for a predictive model.
    - You are a staff data scientist, so you should ask questions that an experienced data scientist would ask.
    """
)

qa_template = (
    """
    You are a very experienced staff data scientist that have been tasked with analyzing a dataset.
    you did the preprocessing steps before and now you are ready to do some feature engineering.
    now you are given a question about the dataset. 

    Dataset information:
    {dataset_info}

    question:
    {question}

    you should answer the question using the dataset and provide the code that you used to answer the question.
    try to provide the answer in a clear and concise way.
    you are a staff data scientist so you should provide the answer in a professional way.

    Important notes:
    - the Dataframe is already loaded in the variable `df`. you don't need to load it again.

    you should provide the answer in the exact following format:
    Title: <title of the answer>
    Description: <description of the answer>
    ```
    code here
    ```
    rest of description if needed.
    """
)


preprocess_template = PromptTemplate(preprocess_template)
feature_eng_template = PromptTemplate(feature_eng_template)
visualization_template = PromptTemplate(visualization_template)
questions_template = PromptTemplate(questions_template)
qa_template = PromptTemplate(qa_template)

