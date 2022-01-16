"""
df836e29_0b20_4e7c_bfa3_2be67f641a51
date created: 2022-01-16 16:57:20.652276
"""
import random

from apps.auth.utils import encode_password


def upgrade(migrator):

    user_count = 10
    for index in range(user_count):
        migrator.execute_sql(
                """
                INSERT into authuser (username, password) 
                values ('{0}', '{1}')
                """.format(f'user{index}@mail.com',
                           encode_password(f'user{index}'))
            )

    for index in range(1000):
        migrator.execute_sql(
            """
            insert into point (name, latitude, longitude)
            values ('{0}', {1}, {2} )
            """.format(
                f'Point {index}',
                random.randint(0, 1000),
                random.randint(0, 1000),
            )
        )

    for route_index in range(random.randint(20, 50)):
        migrator.execute_sql(
            """
            insert into route (name, user_id)
            values ('{0}', {1})
            """.format(
                f'Route {route_index}',
                random.randint(1, user_count)
            )
        )
        for point_index in range(random.randint(2, 100)):
            migrator.execute_sql(
                """
                insert into routeitem (route_id, point_id, "order")
                values ({0}, {1}, {2})
                """.format(
                    route_index + 1,
                    random.randint(1, 1000),
                    point_index,
                )
            )


def downgrade(migrator):
    pass
