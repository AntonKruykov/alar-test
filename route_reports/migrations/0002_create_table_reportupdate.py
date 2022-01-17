"""
create table reportupdate
date created: 2022-01-17 13:05:28.524497
"""


def upgrade(migrator):
    with migrator.create_table('reportupdate') as table:
        table.primary_key('id')
        table.int('report', unique=True)
        table.int('last_id')


def downgrade(migrator):
    migrator.drop_table('reportupdate')
