"""Pydantic-based schema validation before loading."""

from __future__ import annotations

import logging
from typing import Type

import pandas as pd
from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)


def validate_dataframe(
    df: pd.DataFrame,
    schema: Type[BaseModel],
    drop_invalid: bool = True,
) -> pd.DataFrame:
    """Validate each row of *df* against a Pydantic *schema*.

    Parameters
    ----------
    df : pd.DataFrame
    schema : Pydantic BaseModel subclass
    drop_invalid : bool
        If True, drop invalid rows. If False, raise on first error.

    Returns
    -------
    Validated DataFrame (possibly fewer rows if drop_invalid=True).
    """
    valid_idx: list[int] = []

    for idx, row in df.iterrows():
        try:
            schema(**row.to_dict())
            valid_idx.append(idx)
        except ValidationError as exc:
            if not drop_invalid:
                raise
            logger.warning("Row %d failed validation: %s", idx, exc.error_count())

    dropped = len(df) - len(valid_idx)
    if dropped:
        logger.info("Dropped %d / %d invalid rows", dropped, len(df))

    return df.loc[valid_idx].reset_index(drop=True)
