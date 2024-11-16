# # app-source/src/tests/e2e/test_workflow.py
# import asyncio

# import pytest
# from httpx import AsyncClient

# from ...app.config import settings
# from ...app.main import app


# @pytest.mark.asyncio
# async def test_complete_workflow():
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         # Step 1: Create new item
#         create_response = await client.post(
#             "/api/v1/items",
#             headers={"X-API-Key": settings.API_KEY},
#             json={"name": "Test Item", "description": "Test Description"},
#         )
#         assert create_response.status_code == 201
#         item_id = create_response.json()["id"]

#         # Step 2: Verify item exists
#         get_response = await client.get(
#             f"/api/v1/items/{item_id}", headers={"X-API-Key": settings.API_KEY}
#         )
#         assert get_response.status_code == 200
#         assert get_response.json()["name"] == "Test Item"

#         # Step 3: Update item
#         update_response = await client.put(
#             f"/api/v1/items/{item_id}",
#             headers={"X-API-Key": settings.API_KEY},
#             json={"name": "Updated Item", "description": "Updated Description"},
#         )
#         assert update_response.status_code == 200

#         # Step 4: Verify update
#         get_updated = await client.get(
#             f"/api/v1/items/{item_id}", headers={"X-API-Key": settings.API_KEY}
#         )
#         assert get_updated.json()["name"] == "Updated Item"

#         # Step 5: Delete item
#         delete_response = await client.delete(
#             f"/api/v1/items/{item_id}", headers={"X-API-Key": settings.API_KEY}
#         )
#         assert delete_response.status_code == 204

#         # Step 6: Verify deletion
#         get_deleted = await client.get(
#             f"/api/v1/items/{item_id}", headers={"X-API-Key": settings.API_KEY}
#         )
#         assert get_deleted.status_code == 404


# @pytest.mark.asyncio
# async def test_concurrent_operations():
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         # Create multiple items concurrently
#         async def create_item(i):
#             return await client.post(
#                 "/api/v1/items",
#                 headers={"X-API-Key": settings.API_KEY},
#                 json={"name": f"Item {i}", "description": f"Description {i}"},
#             )

#         create_tasks = [create_item(i) for i in range(10)]
#         responses = await asyncio.gather(*create_tasks)

#         assert all(r.status_code == 201 for r in responses)

#         # Get all items
#         list_response = await client.get(
#             "/api/v1/items", headers={"X-API-Key": settings.API_KEY}
#         )
#         assert list_response.status_code == 200
#         assert len(list_response.json()) >= 10
