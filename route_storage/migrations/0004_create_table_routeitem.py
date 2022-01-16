"""
create table routeitem
date created: 2022-01-15 16:56:40.857064
"""


def upgrade(migrator):
    with migrator.create_table('routeitem') as table:
        table.primary_key('id')
        table.foreign_key('AUTO', 'route_id', on_delete=None, on_update=None, references='route.id')
        table.foreign_key('AUTO', 'point_id', on_delete=None, on_update=None, references='point.id')
        table.int('order', null=True)


def downgrade(migrator):
    migrator.drop_table('routeitem')
