from pymongo import MongoClient
import pandas as pd

# MongoDB 서버에 연결 : Both connect in case local and remote
client = MongoClient('mongodb://192.168.0.91:27017/')

# 'mydatabase' 데이터베이스 선택 (없으면 자동 생성)
db = client['mydatabase']

# 'users' 컬렉션 선택 (없으면 자동 생성)
collection_users = db['users_collecting']

# # 입력할 데이터
# user_data = [
#     {"id": 1, "name": "Alice", "age": 25},
#     {"id": 2, "name": "Bob", "age": 30},
#     {"id": 3, "name": "Charlie", "age": 35},
#     {"id": 4, "name": "David", "age": 40},
#     {"id": 1, "name": "Alice", "age": 25}
#     ]

# # 데이터 입력
# result = collection.insert_many(user_data)

# # 입력된 문서의 ID 출력
# print('Inserted user id:', result.inserted_ids)

users_source = collection_users.find({})

# 중복처리
df_data = pd.DataFrame(list(users_source))

# 중복 처리: _id 컬럼을 제외하고 중복 제거
df_unique = df_data.drop_duplicates(subset=['name', 'age'])  # 중복 기준 필드 설정


collection_target = db['users_target']
collection_target.insert_many(df_unique.to_dict('records'))

