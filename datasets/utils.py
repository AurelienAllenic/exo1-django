import json
import numpy as np
import pandas as pd


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return None if (np.isnan(obj) or np.isinf(obj)) else float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def _safe(val):
    if val is None:
        return None
    try:
        f = float(val)
        return None if (np.isnan(f) or np.isinf(f)) else round(f, 4)
    except (TypeError, ValueError):
        return None


def analyze_csv(file_path):
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin-1')

    columns_info = []
    charts = []

    for col in df.columns:
        is_numeric = pd.api.types.is_numeric_dtype(df[col])
        missing = int(df[col].isna().sum())

        col_info = {
            'name': col,
            'dtype': str(df[col].dtype),
            'type': 'numerical' if is_numeric else 'categorical',
            'missing': missing,
            'missing_pct': round(df[col].isna().mean() * 100, 1),
            'unique': int(df[col].nunique()),
        }

        if is_numeric:
            series = df[col].dropna()
            col_info['stats'] = {
                'mean': _safe(series.mean()),
                'std': _safe(series.std()),
                'min': _safe(series.min()),
                'max': _safe(series.max()),
                'median': _safe(series.median()),
                'q25': _safe(series.quantile(0.25)),
                'q75': _safe(series.quantile(0.75)),
            }
            bins_count = min(20, max(5, int(series.nunique() / 2))) if len(series) else 5
            counts, bins = np.histogram(series, bins=bins_count)
            charts.append({
                'column': col,
                'chart_type': 'bar',
                'labels': [f'{bins[i]:.2f}' for i in range(len(bins) - 1)],
                'data': counts.tolist(),
                'title': f'Distribution — {col}',
                'color': 'rgba(54, 162, 235, 0.7)',
                'border_color': 'rgba(54, 162, 235, 1)',
            })
        else:
            vc = df[col].value_counts().head(15)
            charts.append({
                'column': col,
                'chart_type': 'bar',
                'labels': [str(x) for x in vc.index.tolist()],
                'data': [int(x) for x in vc.values.tolist()],
                'title': f'Top valeurs — {col}',
                'color': 'rgba(255, 99, 132, 0.7)',
                'border_color': 'rgba(255, 99, 132, 1)',
            })

        columns_info.append(col_info)

    preview_df = df.head(10).fillna('').astype(str)

    return {
        'shape': {'rows': len(df), 'cols': len(df.columns)},
        'columns_info': columns_info,
        'charts': charts,
        'headers': df.columns.tolist(),
        'preview_rows': preview_df.values.tolist(),
    }
