

class connect_mongo:
    def insert_recode_in_mongo(client, dbname, collectionname, input_list):

        # 'mydatabase' 데이터베이스 선택 (없으면 자동 생성)
        db = client[dbname]
        # 'users' 컬렉션 선택 (없으면 자동 생성)
        collection = db[collectionname]

        # 데이터 입력
        # results = collection.insert_many(input_list)
        results = collection.insert_many(input_list.to_dict(orient='records'))

        return results