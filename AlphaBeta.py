import pandas as pd
import datetime

def set_benchmark(context, data, type='price') :
    benchmarks = data['benchmark'].unique().tolist()
    if len(benchmarks) == 1 :
        if type == 'price' :
            data['return'] = data[context.benchmark]['price'].pct_change(1)
    elif len(benchmarks) > 1 :
        dfs = []
        for benchmark in benchmarks :
            df = data[data['benchmark']==benchmark]
            df['return'] = df['price'].pct_change(1)
            dfs.append(df)
        data = pd.concat(dfs)

    context.benchmark_data = data

def benchmark_return_history(context, benchmarks, indice, periods):
    data = context.benchmark_data
    time_list = [context.current_time - datetime.timedelta(days=x) for x in reversed(range(periods))]
    querydata = data[data['date'].isin(time_list)]
    # 조회시간들에 해당하는 데이터만 필터

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
            # 해당 조건들에 해당하는 스칼라 값을 반환

    return querydata