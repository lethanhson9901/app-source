# # app-source/src/tests/integration/test_database.py
# import asyncpg
# import pytest

# from ...app.config import settings


# @pytest.mark.asyncio
# async def test_database_operations():
#     # Connect to database
#     conn = await asyncpg.connect(settings.DATABASE_URL)

#     try:
#         # Create test table
#         await conn.execute(
#             """
#             CREATE TEMPORARY TABLE test_items (
#                 id SERIAL PRIMARY KEY,
#                 name TEXT NOT NULL,
#                 description TEXT,
#                 created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
#                 updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
#             )
#         """
#         )

#         # Insert test data
#         item_id = await conn.fetchval(
#             """
#             INSERT INTO test_items (name, description)
#             VALUES ($1, $2)
#             RETURNING id
#         """,
#             "Test Item",
#             "Test Description",
#         )

#         # Verify insertion
#         row = await conn.fetchrow("SELECT * FROM test_items WHERE id = $1", item_id)
#         assert row["name"] == "Test Item"
#         assert row["description"] == "Test Description"

#         # Update data
#         await conn.execute(
#             """
#             UPDATE test_items
#             SET name = $1, description = $2
#             WHERE id = $3
#         """,
#             "Updated Item",
#             "Updated Description",
#             item_id,
#         )

#         # Verify update
#         row = await conn.fetchrow("SELECT * FROM test_items WHERE id = $1", item_id)
#         assert row["name"] == "Updated Item"
#         assert row["description"] == "Updated Description"

#         # Delete data
#         await conn.execute("DELETE FROM test_items WHERE id = $1", item_id)

#         # Verify deletion
#         row = await conn.fetchrow("SELECT * FROM test_items WHERE id = $1", item_id)
#         assert row is None

#     finally:
#         await conn.close()


# @pytest.mark.asyncio
# async def test_database_constraints():
#     conn = await asyncpg.connect(settings.DATABASE_URL)

#     try:
#         # Create test table with constraints
#         await conn.execute(
#             """
#             CREATE TEMPORARY TABLE test_items_constraints (
#                 id SERIAL PRIMARY KEY,
#                 name TEXT NOT NULL,
#                 description TEXT,
#                 created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
#                 updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
#                 CONSTRAINT name_length CHECK (char_length(name) >= 3)
#             )
#         """
#         )

#         # Test NOT NULL constraint
#         with pytest.raises(asyncpg.NotNullViolationError):
#             await conn.execute(
#                 """
#                 INSERT INTO test_items_constraints (description)
#                 VALUES ($1)
#             """,
#                 "Test Description",
#             )

#         # Test name length constraint
#         with pytest.raises(asyncpg.CheckViolationError):
#             await conn.execute(
#                 """
#                 INSERT INTO test_items_constraints (name, description)
#                 VALUES ($1, $2)
#             """,
#                 "ab",
#                 "Description too short name",
#             )

#     finally:
#         await conn.close()
