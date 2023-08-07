"""Main functions for coefficient plots (ceofplots) of multiple regression models."""
from typing import Any, List, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd

np.seterr(all="ignore")
import matplotlib.pyplot as plt
from matplotlib.pyplot import Axes
from pyforestplot.arg_validators import check_data
from pyforestplot.dataframe_utils import (
    insert_groups,
    reverse_dataframe,
    sort_data,
    sort_groups,
)
from pyforestplot.graph_utils import (
    despineplot,
    draw_alt_row_colors,
    draw_ci,
    draw_est_markers,
    draw_pval_right,
    draw_ref_xline,
    draw_tablelines,
    draw_xticks,
    draw_ylabel1,
    draw_yticklabel2,
    format_grouplabels,
    format_tableheader,
    format_xlabel,
    format_xticks,
    remove_ticks,
    right_flush_yticklabels,
)
from pyforestplot.text_utils import (
    form_est_ci,
    format_varlabels,
    indent_nongroupvar,
    make_tableheaders,
    normalize_varlabels,
    prep_annote,
    prep_rightannnote,
    star_pval,
)

def mforestplot(
    dataframe: pd.core.frame.DataFrame,
    estimate: str,
    varlabel: str,
    model_col: str,
    models: Optional[Union[Sequence[str], None]] = None,
    modellabels: Optional[Union[Sequence[str], None]] = None,
    moerror: Optional[str] = None,
    ll: Optional[str] = None,
    hl: Optional[str] = None,
    groupvar: Optional[str] = None,
    group_order: Optional[Union[Sequence[str], None]] = None,
    annote: Optional[Union[Sequence[str], None]] = None,
    annoteheaders: Optional[Union[Sequence[str], None]] = None,
    rightannote: Optional[Union[Sequence[str], None]] = None,
    right_annoteheaders: Optional[Union[Sequence[str], None]] = None,
    flush: bool = True,
    decimal_precision: int = 2,
    figsize: Union[Tuple, List] = (4, 8),
    xticks: Optional[Union[list, range]] = None,
    ylabel: Optional[str] = None,
    xlabel: Optional[str] = None,
    yticker2: Optional[str] = None,
    color_alt_rows: bool = False,
    return_df: bool = False,
    preprocess: bool = True,
    **kwargs: Any,
) -> Axes:

    df = check_data(
        dataframe=dataframe,
        estimate=estimate,
        varlabel=varlabel,
        moerror=moerror,
        pval=None,
        ll=ll,
        hl=hl,
        annote=annote,
        annoteheaders=annoteheaders,
        rightannote=rightannote,
        right_annoteheaders=right_annoteheaders,
    )

    if ll is None:
        ll, hl = "ll", "hl"

    if preprocess:
        df = _preprocess_multmodel_dataframe(
            dataframe=dataframe,
            estimate=estimate,
            varlabel=varlabel,
            moerror=moerror,
            model_col=model_col,
            models=models,
            ll=ll,
            hl=hl,
            groupvar=groupvar,
            annote=annote,
            annoteheaders=annoteheaders,
            rightannote=rightannote,
            right_annoteheaders=right_annoteheaders,
            flush=flush,
            decimal_precision=decimal_precision,
            **kwargs,
        )
    # return df, df
    ax = _make_mforestplot(
        dataframe=df,
        yticklabel="yticklabel",
        estimate=estimate,
        moerror=moerror,
        model_col=model_col,
        models=models,
        modellabels=modellabels,
        groupvar=groupvar,
        annoteheaders=annoteheaders,
        rightannote=rightannote,
        right_annoteheaders=right_annoteheaders,
        figsize=figsize,
        xticks=xticks,
        ll=ll,
        hl=hl,
        flush=flush,
        ylabel=ylabel,
        xlabel=xlabel,
        yticker2=yticker2,
        color_alt_rows=color_alt_rows,
        **kwargs,
    )

    return df, ax