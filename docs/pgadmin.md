# pgAdmin

Open <http://localhost:5050> and log in with `PGADMIN_EMAIL` and `PGADMIN_PASSWORD` from `.env`.

## Register the database

| Field                | Value                                |
| -------------------- | ------------------------------------ |
| Host name/address    | `psql_bp`                            |
| Port                 | `5432`                               |
| Maintenance database | `multimodal_vector_search`           |
| Username             | `mvs`                                |
| Password             | `DB_PASSWORD` from `.env`            |
| Save password?       | On                                   |

- The host is `psql_bp`, not `localhost`: pgAdmin runs in its own container, where `localhost` is pgAdmin itself.
- The password is the database one (`DB_PASSWORD`), not the pgAdmin login (`PGADMIN_PASSWORD`).
