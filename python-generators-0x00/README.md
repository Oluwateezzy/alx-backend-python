## How to Use This Implementation

1. **Database Setup**:
   - Run `0-main.py` to create the database and table, and populate it with data
   - The script checks for existing data to avoid duplicates

2. **Streaming Rows**:
   - The `stream_rows()` generator yields one row at a time
   - It uses `fetchmany()` with a batch size of 1 to get rows one by one
   - Each row is returned as a dictionary for easy access to fields

## Key Features:

1. **Memory Efficiency**:
   - The generator streams rows without loading all data into memory
   - Uses server-side cursors for efficient fetching

2. **Error Handling**:
   - Proper connection and cursor management
   - Cleanup in finally blocks

3. **Flexibility**:
   - Can adjust batch_size parameter if needed
   - Returns rows as dictionaries for easy field access

4. **Database Safety**:
   - Checks for existing records before insertion
   - Uses parameterized queries to prevent SQL injection
