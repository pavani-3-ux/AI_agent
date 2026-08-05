
import sqlite3
from datetime import datetime


# ============================================================
# DATABASE SETTINGS
# ============================================================

DATABASE_NAME = "agent_memory.db"


# ============================================================
# CONNECT TO DATABASE
# ============================================================

def get_connection():
    """
    Create a connection to the SQLite database.
    """

    return sqlite3.connect(DATABASE_NAME)


# ============================================================
# CREATE MEMORY TABLE
# ============================================================

def initialize_database():
    """
    Create the memories table if it does not already exist.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


# ============================================================
# SAVE MESSAGE
# ============================================================

def save_memory(role, content):
    """
    Save a user or assistant message into the database.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO memories
        (role, content, created_at)
        VALUES (?, ?, ?)
        """,
        (
            role,
            content,
            datetime.now().isoformat()
        )
    )

    connection.commit()
    connection.close()


# ============================================================
# LOAD ALL MEMORIES
# ============================================================

def load_memories():
    """
    Load all previous conversation messages.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT role, content
        FROM memories
        ORDER BY id ASC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        {
            "role": role,
            "content": content
        }
        for role, content in rows
    ]


# ============================================================
# CLEAR MEMORY
# ============================================================

def clear_memories():
    """
    Delete all stored conversation memory.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM memories"
    )

    connection.commit()
    connection.close()


# ============================================================
# TEST DATABASE
# ============================================================

if __name__ == "__main__":

    print("Initializing database...")

    initialize_database()

    print("Saving test memory...")

    save_memory(
        "user",
        "My name is Pavani."
    )

    save_memory(
        "assistant",
        "Nice to meet you, Pavani!"
    )

    print("\nStored memories:")

    memories = load_memories()

    for memory in memories:
        print(
            f"{memory['role']}: "
            f"{memory['content']}"
        )

    print("\nDatabase test completed successfully.")
