# CRUD Templates

We have templates for CRUD operations that define standard action patterns for different entity types.

## CIDED Template

**Create, Index (list), Details, Edit, Delete**

Standard CRUD template for entities that support full create, read, update, and delete operations.

- **Create**: Create new entity instances
- **Index**: List all entity instances
- **Details**: View a specific entity instance
- **Edit**: Modify an existing entity instance
- **Delete**: Remove an entity instance

## CIDRA Template

**Create, Index, Details, Reject (along with an Edit), Approve**

Template for entities that require approval workflows, such as requests, submissions, or pending records.

- **Create**: Create new entity instances
- **Index**: List all entity instances
- **Details**: View a specific entity instance
- **Reject**: Reject an entity instance (typically includes Edit capability)
- **Approve**: Approve an entity instance

## CID Template

**Create, Index, Details**

Template for readonly entities such as logs, audit trails, or historical records that cannot be modified or deleted after creation.

- **Create**: Create new entity instances
- **Index**: List all entity instances
- **Details**: View a specific entity instance
