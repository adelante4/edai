import pandas as pd


def dataframe_info(df: pd.DataFrame, description: str, column_descriptions: dict[str, str]) -> str:
    info_str = [f"Description: {description}\n", f"DataFrame Shape: {df.shape}\n", "Columns:"]

    for col in df.columns:
        col_type = df[col].dtype
        num_nulls = df[col].isnull().sum()
        unique_vals = df[col].nunique()
        sample_vals = df[col].dropna().unique()[:5]
        sample_vals_str = ", ".join(map(str, sample_vals))

        col_desc = column_descriptions.get(col, "No description provided")

        col_info = (
            f"  - {col}:\n"
            f"    Description: {col_desc}\n"
            f"    Type: {col_type}\n"
            f"    Nulls: {num_nulls}\n"
            f"    Unique Values: {unique_vals}\n"
            f"    Sample Values: {sample_vals_str}\n"
        )

        if pd.api.types.is_numeric_dtype(df[col]) and not pd.api.types.is_bool_dtype(df[col]):
            stats = (
                f"Mean: {df[col].mean():.2f}, "
                f"Median: {df[col].median():.2f}, "
                f"Min: {df[col].min()}, "
                f"Max: {df[col].max()}, "
                f"25th Percentile: {df[col].quantile(0.25):.2f}, "
                f"75th Percentile: {df[col].quantile(0.75):.2f}"
            )
            col_info += f"    Stats: {stats}\n"
        elif pd.api.types.is_categorical_dtype(df[col]) or pd.api.types.is_object_dtype(df[col]):
            top_values = df[col].value_counts().head(5).to_dict()
            top_values_str = ", ".join([f"{k}: {v}" for k, v in top_values.items()])
            mode_value = df[col].mode().iloc[0] if not df[col].mode().empty else "N/A"
            col_info += (
                f"    Top Values: {top_values_str}\n"
                f"    Mode: {mode_value}\n"
            )

        info_str.append(col_info)

    return "\n".join(info_str)
