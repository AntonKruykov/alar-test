"""
218ed402_d84a_49d4_bb01_e019d9b782b1
date created: 2022-01-17 13:06:40.789293
"""


def upgrade(migrator):
    migrator.execute_sql("""
        insert into reportupdate (report, last_id)
        values (1, 0)
    """)


def downgrade(migrator):
    pass
