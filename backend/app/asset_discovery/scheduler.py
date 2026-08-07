"""
Automatic Asset Discovery Scheduler
"""


from apscheduler.schedulers.background import BackgroundScheduler

from app.asset_discovery.services import (
    AssetDiscoveryService
)


scheduler = BackgroundScheduler()



DISCOVERY_TARGETS = [

    {
        "host":"example.com",
        "port":443
    }

]



def run_discovery():


    for target in DISCOVERY_TARGETS:


        try:

            AssetDiscoveryService.scan_asset(

                target["host"],

                target["port"]

            )


        except Exception as e:

            print(
                "Discovery failed",
                e
            )





def start_scheduler():


    scheduler.add_job(

        func=run_discovery,

        trigger="interval",

        hours=24,

        id="asset_discovery"

    )


    scheduler.start()
