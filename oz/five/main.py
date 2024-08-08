import json
import yaml
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.sqltypes import String, Integer, Float, Date, DateTime, Boolean
from faker import Faker
import argparse

# 설정 파일 로드
def load_config(file_path):
    if file_path.endswith('.json'):
        with open(file_path, 'r') as file:
            return json.load(file)
    elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    else:
        raise ValueError("Unsupported file type. Use JSON or YAML.")

# 컬럼 타입에 따른 더미 데이터 생성기
def generate_column_data(col_type):
    faker = Faker()
    
    if isinstance(col_type, String):
        return fake.text(max_nb_chars=col_type.length or 255)
    elif isinstance(col_type, Integer):
        return fake.random_int(min=0, max=10000)
    elif isinstance(col_type, Float):
        return fake.random_number(digits=5, fix_len=False)
    elif isinstance(col_type, Boolean):
        return fake.boolean()
    elif isinstance(col_type, Date):
        return fake.date()
    elif isinstance(col_type, DateTime):
        return fake.date_time()
    else:
        return None  # 또는 기본값으로 채울 수 있음

# 테이블에 맞는 더미 데이터 생성기
def generate_dummy_data(table, num_rows):
    data = []
    for _ in range(num_rows):
        row = {}
        for col in table.columns:
            row[col.name] = generate_column_data(col.type)
        data.append(row)
    return data

# 데이터베이스 연결 설정 및 데이터 삽입
def insert_data(config):
    db_config = config['database']
    engine = create_engine(f"mysql+pymysql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database_name']}")
    metadata = MetaData()
    metadata.reflect(bind=engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    for table_name, table_config in config['tables'].items():
        table = Table(table_name, metadata, autoload_with=engine)
        num_rows = table_config['rows']
        mode = table_config['mode']
        
        if mode == 'replace':
            session.execute(table.delete())
        
        dummy_data = generate_dummy_data(table, num_rows)
        session.execute(table.insert(), dummy_data)
    
    session.commit()
    session.close()

# 메인 함수
def main():
    parser = argparse.ArgumentParser(description='Generate and insert dummy data into MySQL tables.')
    parser.add_argument('config', type=str, help='Path to the configuration file (JSON or YAML).')
    args = parser.parse_args()
    
    config = load_config(args.config)
    insert_data(config)

if __name__ == '__main__':
    main()