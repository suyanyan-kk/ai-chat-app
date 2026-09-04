# Knowledge User Isolation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Bind knowledge data to its owner, enforce owner-scoped queries, and require `knowledge.write` for mutations while allowing members to write.

**Architecture:** Store `user_id` on knowledge nodes, uploaded files, and chunks so every independently queried record can be scoped without trusting client input. Resolve ownership exclusively from the authenticated user, reject cross-user file and parent references, and apply the existing permission dependency to mutation endpoints.

**Tech Stack:** FastAPI, SQLAlchemy, Pydantic, unittest/TestClient

---

### Task 1: Define ownership and default permission

**Files:**
- Modify: `app/knowledgedb/models.py`
- Modify: `app/auth/service.py`

1. Add indexed `user_id` foreign keys to the three knowledge tables.
2. Add `knowledge.write` to the member role.
3. Verify role bootstrap tests.

### Task 2: Persist and enforce ownership

**Files:**
- Modify: `app/api/knowledge.py`
- Modify: `app/rag/file/file_service.py`
- Modify: `app/rag/chunk/chunk_service.py`

1. Derive `user_id` from `get_current_user` for every write.
2. Filter lists, details, chunks, updates, and deletes by `user_id`.
3. Validate parent and uploaded-file references belong to the same user.
4. Persist `user_id` into file/chunk records and Chroma metadata.
5. Require `knowledge.write` on POST, PUT, and DELETE routes.

### Task 3: Preserve existing installations

**Files:**
- Modify: `app/auth/bootstrap.py`

1. Detect legacy knowledge tables without `user_id`.
2. Add nullable ownership columns and indexes during startup; legacy unowned rows remain inaccessible.

### Task 4: Verify isolation and permissions

**Files:**
- Create: `tests/test_knowledge_api.py`
- Modify: `tests/test_auth_api.py`

1. Test member role contains `knowledge.write`.
2. Test list/detail/update/delete cannot access another user's nodes.
3. Test cross-user parent/file associations are rejected.
4. Run the full test suite.
