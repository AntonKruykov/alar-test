"""
create table authuser
date created: 2022-01-15 11:13:06.766615
"""


def upgrade(migrator):
    with migrator.create_table('authuser') as table:
        table.primary_key('id')
        table.char('username', index=True, max_length=100, unique=True)
        table.char('password', max_length=128)


def downgrade(migrator):
    migrator.drop_table('authuser')
