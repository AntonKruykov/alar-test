import yaml

from apps.app import make_application


async def run_application():
    """Create app for async manager.

    Example: `gunicorn asgi:run_application`.
    For more detail: https://aiohttp.readthedocs.io/en/stable/deployment.html

    """
    with open('config.yml', 'r') as ymlfile:
        settings = yaml.safe_load(ymlfile)

    return await make_application(settings)
