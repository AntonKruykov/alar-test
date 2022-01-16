"""
create table routereport
date created: 2022-01-16 23:10:38.914306
"""


def upgrade(migrator):
    with migrator.create_table('routereport') as table:
        table.primary_key('id')
        table.int('user_id', unique=True)
        table.char('username', max_length=100, unique=True)
        table.int('route_count')
        table.int('route_length')


def downgrade(migrator):
    migrator.drop_table('routereport')
