"""
Database Viewer for RevampBot
View and manage your bot's database
"""

import sqlite3
import sys

def view_tables(db_path="revampbot.db"):
    """Display all tables and their row counts"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\n" + "=" * 70)
    print("🗄️  REVAMPBOT DATABASE OVERVIEW")
    print("=" * 70)
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    print(f"\n📊 Database: {db_path}")
    print(f"📋 Total Tables: {len(tables)}\n")
    
    for (table_name,) in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  ✓ {table_name:25} [{count:>5} rows]")
    
    conn.close()

def view_table_schema(table_name, db_path="revampbot.db"):
    """Display table structure"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"\n" + "=" * 70)
    print(f"📋 TABLE SCHEMA: {table_name}")
    print("=" * 70 + "\n")
    
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    print(f"{'Column':<20} {'Type':<15} {'Not Null':<10} {'Default':<15} {'PK'}")
    print("-" * 70)
    
    for col in columns:
        cid, name, type_, notnull, dflt_value, pk = col
        print(f"{name:<20} {type_:<15} {str(bool(notnull)):<10} {str(dflt_value):<15} {str(bool(pk))}")
    
    conn.close()

def view_table_data(table_name, limit=10, db_path="revampbot.db"):
    """Display data from a table"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
        rows = cursor.fetchall()
        
        print(f"\n" + "=" * 70)
        print(f"📊 TABLE DATA: {table_name} (showing {len(rows)} rows)")
        print("=" * 70 + "\n")
        
        if rows:
            # Print column headers
            headers = rows[0].keys()
            header_line = " | ".join(f"{h[:15]:<15}" for h in headers)
            print(header_line)
            print("-" * len(header_line))
            
            # Print rows
            for row in rows:
                values = []
                for key in headers:
                    val = row[key]
                    if val is None:
                        val = "NULL"
                    val_str = str(val)[:15]
                    values.append(f"{val_str:<15}")
                print(" | ".join(values))
        else:
            print("⚠️  No data in this table")
            
    except sqlite3.Error as e:
        print(f"❌ Error: {e}")
    
    conn.close()

def main():
    print("\n🤖 RevampBot Database Viewer")
    
    if len(sys.argv) < 2:
        view_tables()
        print("\n💡 Usage:")
        print(f"  python {sys.argv[0]} tables           - View all tables")
        print(f"  python {sys.argv[0]} schema <table>   - View table schema")
        print(f"  python {sys.argv[0]} data <table>     - View table data")
        print(f"  python {sys.argv[0]} data <table> 20  - View 20 rows")
        return
    
    command = sys.argv[1].lower()
    
    if command == "tables":
        view_tables()
    
    elif command == "schema" and len(sys.argv) > 2:
        table_name = sys.argv[2]
        view_table_schema(table_name)
    
    elif command == "data" and len(sys.argv) > 2:
        table_name = sys.argv[2]
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        view_table_data(table_name, limit)
    
    else:
        print("❌ Invalid command or missing arguments")
        print("\n💡 Valid commands:")
        print("  tables, schema <table>, data <table> [limit]")
    
    print()

if __name__ == "__main__":
    main()
