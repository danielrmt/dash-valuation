import numpy as np

import dash_html_components as html
import dash_bootstrap_components as dbc


def calc_kpis(df, quarterly=True):
    df.sort_values('DT_FIM_EXERC', inplace=True)
    df['ShareholderEquity'] = \
        df['StakeholderEquity'] - df['MinorityInterests'].fillna(0)
    df['NetDebt'] = df['Debt'].fillna(0) - df['Cash']
    df['InvestedCapital'] = df['ShareholderEquity'] + df['Debt'].fillna(0)
    df['GrossMargin'] = 100 * df['GrossProfit'] / df['Revenue']
    df['EBITMargin'] = 100 * df['EBIT'] / df['Revenue']
    df['NetMargin'] = 100 * df['NetIncome'] / df['Revenue']
    df['DebtToEquity'] = np.where(df['ShareholderEquity'] < 0, np.NaN,
                                  df['Debt'] / df['ShareholderEquity'])
    df['DebtToCapital'] = df['Debt'] / df['InvestedCapital']

    if quarterly:
        df['LTM_NetIncome'] = df['NetIncome'].rolling(4).sum()
        df['LTM_EBIT'] = df['EBIT'].rolling(4).sum()
        df['LTM_ShareholderEquity'] = df['ShareholderEquity'].rolling(4).mean()
        df['LTM_InvestedCapital'] = df['InvestedCapital'].rolling(4).mean()
        df['ROE'] = 100 * df['LTM_NetIncome'] / df['LTM_ShareholderEquity']
        df['ROIC'] = 100 * df['LTM_EBIT'] / df['LTM_InvestedCapital']
        df['NetDebtToEBIT'] = np.where(df['LTM_EBIT'] < 0, np.NaN,
                                   100 * df['NetDebt'] / df['LTM_EBIT'])
    else:
        df['ROE'] = 100 * df['NetIncome'] / df['ShareholderEquity']
        df['ROIC'] = 100 * df['EBIT'] / df['InvestedCapital']
        df['NetDebtToEBIT'] = np.where(df['EBIT'] < 0, np.NaN,
                                   100 * df['NetDebt'] / df['EBIT'])
    return df


#
def grid(rows):
    return html.Div([
        dbc.Row([
            dbc.Col(col, width=12/len(row))
            for col in row
        ])
        for row in rows
    ])
