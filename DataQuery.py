import pandas as pd
import datetime


class DataQuery :
    def __init__(self, data, context) :
        self.data = data
        self.current_time = context.current_time
        # 실제 데이터 프레임(data 인자), 현재시간을(current_time 인자) 클래스 인자로 정의
        # data는 열이 'symbol', 'price', 그리고 사용자가 정의한 fators(여러개일수 있음)로 구성됨


    def current_data(self, symbols, factors) :
        # symbols와 factors는 스칼라 문자 또는 리스트 형태로 넣어줄 수 있음

        querydata = self.data[self.data['date'] == self.current_time]
        # 현재시간에 해당하는 데이터만 필터

        if isinstance(symbols, list) :
            if isinstance(factors, list) :
            # symbols와 factors 모두 리스트 형태로 넣어준 것이라면
                columns = ['symbol']+factors
                # 조회하고자하는 데이터 컬럼 정의

            else :
            # symbols는 리스트, factors는 스칼라 문자형태로 넣어준 것이라면

                columns= ['symbol', factors]
                # 조회하고자하는 데이터 컬럼 정의

            querydata = querydata[querydata['symbol'].isin(symbols)][columns]
            # 해당 조건들에 해당하는 데이터프레임 반환

        else :
            if isinstance(factors, list) :
            # symbols는 스칼라 문자형태, factors는 리스트 형태로 넣어준 것이라면

                querydata = querydata[querydata['symbol'] == symbols][factors]
                # 해당 조건들에 해당하는 데이터프레임 반환

            else :
            # symbols와 factors 모두 스칼라 문자형태로 넣어준 것이라면
                querydata = querydata[querydata['symbol']==symbols][factors].values[0]
                # 해당 조건들에 해당하는 스칼라 값을 반환

        return querydata

    def history(self, symbols, factors, periods) :
        # symbols와 factors는 스칼라 문자 또는 리스트 형태로 넣어줄 수 있음

        time_list = [self.current_time - datetime.timedelta(days=x) for x in reversed(range(periods))]
        querydata = self.data[self.data['date'].isin(time_list)]
        # 조회시간들에 해당하는 데이터만 필터

        if isinstance(symbols, list) :
            if isinstance(factors, list) :
            # symbols와 factors 모두 리스트 형태로 넣어준 것이라면
                columns = ['symbol']+factors
                # 조회하고자하는 데이터 컬럼 정의

            else :
            # symbols는 리스트, factors는 스칼라 문자형태로 넣어준 것이라면

                columns= ['symbol', factors]
                # 조회하고자하는 데이터 컬럼 정의

            querydata = querydata[querydata['symbol'].isin(symbols)][columns]
            # 해당 조건들에 해당하는 데이터프레임 반환

        else :
            if isinstance(factors, list) :
            # symbols는 스칼라 문자형태, factors는 리스트 형태로 넣어준 것이라면

                querydata = querydata[querydata['symbol'] == symbols][factors]
                # 해당 조건들에 해당하는 데이터프레임 반환

            else :
            # symbols와 factors 모두 스칼라 문자형태로 넣어준 것이라면
                querydata = querydata[querydata['symbol']==symbols][factors]
                # 해당 조건들에 해당하는 스칼라 값을 반환

        return querydata