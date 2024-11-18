import pandas as pd

class connect_mongo:
    def insert_recode_in_mongo(client, dbname, collectionname, input_list):

        # 'mydatabase' 데이터베이스 선택 (없으면 자동 생성)
        db = client[dbname]
        # 'users' 컬렉션 선택 (없으면 자동 생성)
        collection = db[collectionname]

        # 데이터 입력
        if isinstance(input_list, pd.DataFrame): # DataFrame인 경우
            results = collection.insert_many(input_list.to_dict(orient='records'))
        elif isinstance(input_list, list): # 리스트인 경우
            results = collection.insert_many(input_list)
        elif isinstance(input_list, dict): # 딕셔너리인 경우
            results = collection.insert_one(input_list)
        else:
            print("error")

        return results

        return results