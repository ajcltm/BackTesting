import pandas as pd
import numpy as np
import datetime
from sklearn.linear_model import LinearRegression

class AlphaBeta :

    def __init__(self, context, benchmark_data, type='price'):

        benchmark_symbols = benchmark_data['benchmark'].unique().tolist()

        if len(benchmark_symbols) == 1 :
            benchmark_symbols = benchmark_symbols[0]
            if type == 'price' :
                benchmark_data['return'] = benchmark_data[benchmark_data['benchmark']==benchmark_symbols]['price'].pct_change(1)
        elif len(benchmark_symbols) > 1 :
            dfs = []
            for benchmark in benchmark_symbols :
                df = benchmark_data[benchmark_data['benchmark']==benchmark]
                df['return'] = df['price'].pct_change(1)
                dfs.append(df)
            benchmark_data = pd.concat(dfs)

        context.benchmark['benchmark_symbols'] = benchmark_symbols
        print('context.benchmarks symbols : {0}'.format(context.benchmark['benchmark_symbols']))
        context.benchmark['benchmark_data'] = benchmark_data
        print('context.benchmark_data : \n{0}'.format(context.benchmark['benchmark_data']))

        self.reg = LinearRegression()

        self.querydata = 0

    def benchmark_history(self, context, benchmarks, indice, periods):
        benchmark_data = context.benchmark['benchmark_data']
        time_list = [context.current_time - datetime.timedelta(days=x) for x in reversed(range(periods))]
        print('periods : {0}'.format(periods))
        print('time_list : {0}'.format(time_list))
        querydata = benchmark_data[benchmark_data['date'].isin(time_list)]
        # 조회시간들에 해당하는 데이터만 필터
        print('querydata : \n{0}'.format(querydata))

        if isinstance(benchmarks, list):
            if isinstance(indice, list):
                # benchmarks와 factors 모두 리스트 형태로 넣어준 것이라면
                columns = ['benchmark'] + indice
                # 조회하고자하는 데이터 컬럼 정의

            else:
                # benchmarks는 리스트, indice는 스칼라 문자형태로 넣어준 것이라면

                columns = ['benchmark', indice]
                # 조회하고자하는 데이터 컬럼 정의

            querydata = querydata[querydata['benchmark'].isin(benchmarks)][columns]
            # 해당 조건들에 해당하는 데이터프레임 반환

        else:
            if isinstance(indice, list):
                # benchmarks는 스칼라 문자형태, indice는 리스트 형태로 넣어준 것이라면

                querydata = querydata[querydata['benchmark'] == benchmarks][indice]
                # 해당 조건들에 해당하는 데이터프레임 반환

            else:
                # benchmarks와 indice 모두 스칼라 문자형태로 넣어준 것이라면
                querydata = querydata[querydata['benchmark'] == benchmarks][indice]
                # 해당 조건들에 해당하는 시리즈를 반환 (조회되는 date가 여럿이기 때문에 스칼라가 아닌 시리즈 형태로 반환)

        self.querydata = querydata

        return querydata

    def get_alpha_beta(self, y):
        x = self.querydata.values.reshape(-1,1)
        x = np.delete(x, 0, 0)
        print('x : \n{0}'.format(y))

        alpha_beta = self.reg.fit(x, y)
        alpha = alpha_beta.intercept_[0]
        beta = alpha_beta.coef_[0][0]

        return alpha, beta
