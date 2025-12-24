import re
import os
from langchain_community.utilities import SQLDatabase
from langchain.tools import tool

# Ensure the database path is absolute to avoid "no such table" errors
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "..", "data", "company_records.db")
db = SQLDatabase.from_uri(f"sqlite:///{os.path.abspath(db_path)}")

@tool
def internal_database_tool(input_text: str) -> str:
    """
    Query company data. Tables: 
    - employees (id, name, department, salary, hire_date)
    - sales (sale_id, item_name, category, amount, sale_date, region)
    Input: Raw SQL string only.
    """
    # 1. Clean brackets and variable names like 'sql_query ='
    clean_sql = str(input_text).strip("[]'\" ")
    prefixes = [r'^sql_query\s*=\s*', r'^query\s*=\s*', r'^sql\s*=\s*']
    for p in prefixes:
        clean_sql = re.sub(p, '', clean_sql, flags=re.IGNORECASE)
    
    # 2. Strip Markdown code blocks
    clean_sql = re.sub(r'```sql|```', '', clean_sql).strip()
    
    try:
        # 3. Execute
        print(f"\n[DB LOG] Executing: {clean_sql}")
        return db.run(clean_sql)
    except Exception as e:
        return f"SQL Error: {e}. Use simple SELECT statements."

tools = [internal_database_tool]