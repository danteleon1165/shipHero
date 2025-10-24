from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.jobs.edi_sync import poll_sps_orders
import atexit


scheduler = BackgroundScheduler()


def setup_scheduler(app):
    """Setup APScheduler for background jobs."""
    
    with app.app_context():
        # Schedule EDI order polling every 5 minutes
        scheduler.add_job(
            func=lambda: poll_sps_orders(app),
            trigger=IntervalTrigger(minutes=5),
            id='poll_sps_orders',
            name='Poll SPS Commerce for new orders',
            replace_existing=True
        )
        
        # Start scheduler
        if not scheduler.running:
            scheduler.start()
            app.logger.info('Background scheduler started')
        
        # Shutdown scheduler on app exit
        atexit.register(lambda: scheduler.shutdown())
