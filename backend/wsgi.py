from app import create_app


app = create_app()


from app.asset_discovery.scheduler import start_scheduler

start_scheduler()
