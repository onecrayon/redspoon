from alembic import op


def ensure_uuids_available():
    """Ensures that we can generate UUIDs in PostgreSQL"""
    op.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto')


def create_trigger_for_table(tablename):
    """Creates a trigger on insert for the given table to automatically add a global UUID"""
    # Create or update our trigger function
    op.execute("""
    CREATE OR REPLACE FUNCTION generate_global_uuid() RETURNS trigger AS $generate_global_uuid$
        DECLARE _newUuid UUID;
        BEGIN
            IF NEW.uuid IS NOT NULL THEN
                RAISE EXCEPTION 'uuid must be null on insert';
            END IF;
            
            INSERT INTO global_uuids (data_type)
                VALUES (TG_TABLE_NAME::regclass::text)
                RETURNING uuid INTO _newUuid;
            NEW.uuid := _newUuid;
            RETURN NEW;
        END;
    $generate_global_uuid$ LANGUAGE plpgsql;
    """)
    # And now hook it up to our new table
    op.execute(f"""
    CREATE TRIGGER generate_global_uuid_{tablename} BEFORE INSERT ON {tablename}
        FOR EACH ROW EXECUTE FUNCTION generate_global_uuid();
    """)


def drop_trigger_for_table(tablename):
    """Drops the UUID on insert trigger for the given tablename"""
    op.execute(f'DROP TRIGGER IF EXISTS generate_global_uuid_{tablename} ON {tablename}')
