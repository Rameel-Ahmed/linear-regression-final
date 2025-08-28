"""backend.utils.csv_loader
+------------------------------------------------
Load, inspect, and clean CSV datasets prior to linear-regression training.

* Duplicate, outlier, and NaN removal.
* Coercion of numeric-looking strings.
* Compact, human-readable cleaning summary for UI display.

 We normalize before training to improve
numerical stability; after training, predictions are mapped
back to the original scale (denormalize) for interpretability.


Example
-------
>>> import pandas as pd
>>> from backend.utils.csv_loader import CSVLoader
>>> df = pd.DataFrame({"x": [1, 2, 2, 3], "y": [2, 4, 4, 6]})
>>> loader = CSVLoader("x", "y")
>>> quality = loader.analyze_data_quality(df)
>>> clean = loader.clean_data(df)
>>> loader.get_cleaning_summary()["samples_removed"]
1
"""

import numpy as np
import pandas as pd
from typing import Any


class CSVLoader:
    """Load and clean CSV data for linear regression tasks."""

    def __init__(self, x_column: str, y_column: str) -> None:
        """Initialize loader with names of x and y columns."""
        # Internal-only attributes -> double-underscore
        self.__x_colname: str = x_column
        self.__y_colname: str = y_column
        self.__cleaning_summary: dict[str, Any] = {}

    def analyze_data_quality(self, df: pd.DataFrame) -> dict[str, Any]:
        """
        Analyze data quality without mutating the DataFrame.

        Returns a summary dict listing duplicates, missing cells,
        and counts of non-numeric strings in the configured columns.
        """
        try:
            analysis: dict[str, Any] = {
                "total_rows": len(df),
                "x_column": self.__x_colname,
                "y_column": self.__y_colname,
                "summary": [],
            }

            # duplicates
            dup_count: int = int(df.duplicated().sum())
            if dup_count > 0:
                analysis["summary"].append(f"{dup_count} rows have duplicates")

            # missing
            x_missing: int = int(df[self.__x_colname].isna().sum())
            y_missing: int = int(df[self.__y_colname].isna().sum())
            if x_missing > 0:
                analysis["summary"].append(f"{x_missing} rows have NaN in X column")
            if y_missing > 0:
                analysis["summary"].append(f"{y_missing} rows have NaN in Y column")

            # non-numeric string check (skip numeric-looking strings)
            x_col = df[self.__x_colname]
            y_col = df[self.__y_colname]

            x_strings: int = sum(
                1
                for val in x_col
                if isinstance(val, str)
                and not str(val).replace(".", "").replace("-", "").isdigit()
            )
            y_strings: int = sum(
                1
                for val in y_col
                if isinstance(val, str)
                and not str(val).replace(".", "").replace("-", "").isdigit()
            )

            if x_strings:
                if x_strings == len(df):
                    analysis["summary"].append("X column is all string")
                else:
                    analysis["summary"].append(
                        f"{x_strings} rows have string in X column"
                    )

            if y_strings:
                if y_strings == len(df):
                    analysis["summary"].append("Y column is all string")
                else:
                    analysis["summary"].append(
                        f"{y_strings} rows have string in Y column"
                    )

            if not analysis["summary"]:
                analysis["summary"].append("Data looks clean!")

            return analysis

        except Exception as exc:
            # Return structured message rather than crash caller
            return {"error": True, "message": f"Analysis failed: {exc}"}

    def clean_data(
        self,
        df: pd.DataFrame,
        remove_duplicates: bool = True,
        remove_outliers: bool = False,
        handle_missing: str = "remove",
        remove_strings: bool = True,
    ) -> pd.DataFrame:
        """
        Clean a DataFrame of the configured x and y columns.

        This method applies requested operations in order and then
        validates the result. It raises RuntimeError on unrecoverable
        failures so calling code may present the error to users.
        """
        df_clean: pd.DataFrame = df.copy()
        try:
            if remove_duplicates:
                df_clean = self.__remove_duplicates(df_clean)

            if remove_outliers:
                df_clean = self.__remove_outliers(df_clean)

            if handle_missing == "remove":
                df_clean = self.__handle_missing_values(df_clean)

            if remove_strings:
                df_clean = self.__remove_string_columns(df_clean)

            # Validate final dataset
            self.__validate_cleaned_data(df_clean)

            # Update summary after all operations
            self.__update_cleaning_summary(
                original=df,
                cleaned=df_clean,
                cleaning_options={
                    "remove_duplicates": remove_duplicates,
                    "remove_outliers": remove_outliers,
                    "handle_missing": handle_missing,
                    "remove_strings": remove_strings,
                },
            )

            return df_clean

        except Exception as exc:
            raise RuntimeError(f"Data cleaning failed: {exc}") from exc

    def get_cleaning_summary(self) -> dict[str, Any]:
        """Alias for :pyattr:`cleaning_summary` property (kept for legacy)."""
        return self.cleaning_summary

    @property
    def cleaning_summary(self) -> dict[str, Any]:
        """Read-only view of the most-recent cleaning summary."""
        return dict(self.__cleaning_summary)

    def __remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate rows and note how many were dropped."""
        initial: int = len(df)
        df_clean: pd.DataFrame = df.drop_duplicates()
        removed: int = initial - len(df_clean)
        if removed > 0:
            self.__cleaning_summary["duplicates_removed"] = removed
        return df_clean

    def __remove_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove outliers from x and y using the IQR method.

        If the column is non-numeric, the method skips outlier removal
        for that column rather than raising an error.
        """
        df_clean: pd.DataFrame = df.copy()
        initial: int = len(df_clean)

        for col in (self.__x_colname, self.__y_colname):
            if col not in df_clean.columns:
                continue
            try:
                Q1: float = float(df_clean[col].quantile(0.25))
                Q3: float = float(df_clean[col].quantile(0.75))
                IQR: float = Q3 - Q1
                lower: float = Q1 - 1.5 * IQR
                upper: float = Q3 + 1.5 * IQR
                df_clean = df_clean[(df_clean[col] >= lower) & (df_clean[col] <= upper)]
            except Exception:
                # Non-numeric or other issue: skip outlier pass for this col
                continue

        removed: int = initial - len(df_clean)
        if removed > 0:
            self.__cleaning_summary["outliers_removed"] = removed
        return df_clean

    def __handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Drop rows with missing x or y values and record count."""
        initial: int = len(df)
        df_clean: pd.DataFrame = df.dropna(subset=[self.__x_colname, self.__y_colname])
        removed: int = initial - len(df_clean)
        if removed > 0:
            self.__cleaning_summary["missing_values_removed"] = removed
        return df_clean

    def __remove_string_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Coerce configured x and y to numeric, then keep numeric cols.

        This ensures we attempt to salvage numeric-looking strings;
        truly non-numeric columns are removed.
        """
        numeric_cols: list[str] = df.select_dtypes(include=[np.number]).columns.tolist()
        # Try coercion for x and y
        for col in (self.__x_colname, self.__y_colname):
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
                if col not in numeric_cols:
                    numeric_cols.append(col)

        df_clean: pd.DataFrame = df[numeric_cols].dropna(
            subset=[self.__x_colname, self.__y_colname]
        )

        removed_count: int = len(df.columns) - len(df_clean.columns)
        if removed_count > 0:
            self.__cleaning_summary["string_columns_removed"] = removed_count
        return df_clean

    def __validate_cleaned_data(self, df: pd.DataFrame) -> None:
        """Ensure the cleaned DataFrame is suitable for training."""
        if df.empty:
            raise ValueError("Cleaning resulted in empty dataset")

        if len(df) < 10:
            raise ValueError("Cleaned dataset too small (minimum 10 samples required)")

        # NaN/infinite checks on target columns
        if df[self.__x_colname].isna().any() or df[self.__y_colname].isna().any():
            raise ValueError("Data contains NaN values after cleaning")

        if np.isinf(df[self.__x_colname]).any() or np.isinf(df[self.__y_colname]).any():
            raise ValueError("Data contains infinite values")

    def __update_cleaning_summary(
        self,
        original: pd.DataFrame,
        cleaned: pd.DataFrame,
        cleaning_options: dict[str, Any],
    ) -> None:
        """Store final cleaning metadata for later retrieval."""
        self.__cleaning_summary.update(
            {
                "original_shape": original.shape,
                "cleaned_shape": cleaned.shape,
                "samples_removed": len(original) - len(cleaned),
                "cleaning_options_applied": cleaning_options,
                "final_columns": cleaned.columns.tolist(),
            }
        )
