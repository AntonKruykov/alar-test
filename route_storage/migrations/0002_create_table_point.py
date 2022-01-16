"""
create table point
date created: 2022-01-15 16:50:48.184319
"""


def upgrade(migrator):
    with migrator.create_table('point') as table:
        table.primary_key('id')
        table.char('name', index=True, max_length=100, unique=True)
        table.int('latitude')
        table.int('longitude')


def downgrade(migrator):
    migrator.drop_table('point')
