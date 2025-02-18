from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, MetaData,select, Table
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# MySQL Database Configuration
# username = 'root'
# password = ''
# server = 'localhost'

# Database configurations
SOURCE_DB_URI = 'mysql+pymysql://root:8861@localhost/sakila'
DESTINATION_DB_URI = 'mysql+pymysql://root:8861@localhost/database2'

# Create database engines
source_engine = create_engine(SOURCE_DB_URI)
destination_engine = create_engine(DESTINATION_DB_URI)

# Create sessions
SourceSession = sessionmaker(bind=source_engine)
DestinationSession = sessionmaker(bind=destination_engine)

app.config['SQLALCHEMY_DATABASE_URI'] = SOURCE_DB_URI 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

def transfer_table(table_name, limit_rows=None):
    metadata = MetaData()
    metadata.reflect(bind=source_engine, only=[table_name])
    source_table = Table(table_name, metadata, autoload_with=source_engine)
    
    with source_engine.connect() as source_conn:
        query = select(source_table)
        if limit_rows:
            query = query.limit(limit_rows)
        result = source_conn.execute(query).fetchall()
    
    metadata_dest = MetaData()
    metadata_dest.reflect(bind=destination_engine)

    if table_name not in metadata_dest.tables:
      with destination_engine.connect() as dest_conn:
          source_table.metadata.create_all(dest_conn)
    
    metadata_dest.reflect(bind=destination_engine)  # Refresh metadata after creation
    
    metadata.reflect(bind=destination_engine)
    dest_table = Table(table_name, metadata, autoload_with=destination_engine)
    
    with destination_engine.connect() as dest_conn:
        dest_conn.execute(dest_table.insert(), [row._asdict() for row in result])
    
    return f"Transferred {len(result)} rows from {table_name}"

@app.route('/transfer1', methods=['POST'])
def transfer1():
    data = request.json
    tables = data.get('tables', [])
    limit_rows = data.get('limit_rows')
    
    if not tables:
        return jsonify({"error": "No tables specified"}), 400
    
    transfer_results = {}
    for table in tables:
        try:
            transfer_results[table] = transfer_table(table, limit_rows)
        except Exception as e:
            transfer_results[table] = f"Error: {str(e)}"
    
    return jsonify(transfer_results)


@app.route('/tables', methods=['GET'] )
def test_db():
    is_source = request.args.get('type')
    try:
        with source_engine.connect() if is_source =='source' else destination_engine.connect()  as conn:
           query = text("SHOW TABLES")
           result = result = conn.execute(query)
           print(result)
           tables = [row[0] for row in result]
           return {"tables": tables}
    
    except Exception as e:
        return f"Database connection failed: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)
