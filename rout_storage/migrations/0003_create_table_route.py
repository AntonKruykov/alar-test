"""
create table route
date created: 2022-01-15 16:54:25.804315
"""


def upgrade(migrator):
    with migrator.create_table('route') as table:
        table.primary_key('id')
        table.foreign_key('AUTO', 'user_id', on_delete=None, on_update=None, references='authuser.id')
        table.char('name', index=True, max_length=100, unique=True)


def downgrade(migrator):
    migrator.drop_table('route')
