from asyncio import get_event_loop

import yaml
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from peewee_async import Manager, PooledPostgresqlDatabase


class SchedulerManager(object):
    """Apscheduler wrapper."""

    def __init__(self) -> None:
        """Init."""
        with open('config.yml', 'r') as ymlfile:
            self.settings = yaml.safe_load(ymlfile)
        self.loop = get_event_loop()
        self.database = self._get_db_pool()
        self.scheduler = AsyncIOScheduler()

    def add_task(self, *args, **kwargs) -> None:
        """Add task wrapper."""
        self.scheduler.add_job(*args, **kwargs)

    def run(self) -> None:
        """Run scheduler in event loop."""
        self.scheduler.print_jobs()
        try:
            self.scheduler.start()
            self.loop.run_forever()
        except (KeyboardInterrupt, SystemExit):
            self.scheduler.shutdown()

    def _get_db_pool(self) -> Manager:
        """Fetch db pool instance."""
        database = PooledPostgresqlDatabase(None)
        database.init(**self.settings['database'])
        database.set_allow_sync(False)
        return Manager(database, loop=self.loop)


scheduler = SchedulerManager()
