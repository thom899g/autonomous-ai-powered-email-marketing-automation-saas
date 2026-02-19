from connectors.mailchimp import MailchimpConnector
from connectors.sendgrid import SendGridConnector
from ai_engine import AIEngine
from optimizer import CampaignOptimizer
from scheduler import TaskScheduler
from monitoring.prometheus import PrometheusMonitor
from dashboard.dashboard import DashboardServer
import logging
from typing import Dict, Any

# Initialize loggers
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AutonomousEmailMarketingSystem:
    def __init__(self):
        self.connectors: Dict[str, Any] = {
            'mailchimp': MailchimpConnector(),
            'sendgrid': SendGridConnector()
        }
        self.ai_engine = AIEngine()
        self.optimizer = CampaignOptimizer()
        self.scheduler = TaskScheduler()
        self.monitor = PrometheusMonitor()
        self.dashboard = DashboardServer()

    def run(self):
        try:
            # Initialize all components
            for name, connector in self.connectors.items():
                logger.info(f"Initializing {name} connector")
                connector.initialize()

            logger.info("Starting monitoring service")
            self.monitor.start()

            logger.info("Starting dashboard server")
            self.dashboard.start()

            logger.info("Scheduling tasks")
            self.scheduler.schedule_task(self.run_optimization_loop, "every_12_hours", name="optimization_loop")
            self.scheduler.schedule_task(self.send_email_campaigns, "every_day_at_8am", name="daily_campaigns")

            logger.info("System ready and running")
        except Exception as e:
            logger.error(f"Failed to initialize system: {str(e)}")
            raise

    def run_optimization_loop(self):
        try:
            logger.info("Starting optimization loop")
            campaigns = self.get_all_campaigns()
            optimized_campaigns = self.ai_engine.optimize_campaigns(campaigns)
            self.optimizer.apply_changes(optimized_campaigns)
            logger.info(f"Optimized {len(optimized_campaigns)} campaigns successfully")
        except Exception as e:
            logger.error(f"Optimization loop failed: {str(e)}")

    def send_email_campaigns(self):
        try:
            logger.info("Starting email sending process")
            campaign = self.get_next_campaign()
            connector = self._get_connector(campaign)
            
            if not connector:
                logger.error("No valid connector found for this campaign")
                return

            # Prepare email content
            personalized_emails = self.ai_engine.personalize_email(campaign)
            
            # Send emails in batches
            success, failures = connector.send_batch(personalized_emails)
            logger.info(f"Successfully sent {success} emails with {failures} failures")
        except Exception as e:
            logger.error(f"Email sending failed: {str(e)}")

    def get_all_campaigns(self):
        # This would fetch all campaigns from the system
        pass

    def _get_connector(self, campaign):
        # Determine which connector to use based on campaign settings
        pass

# Example usage
if __name__ == "__main__":
    try:
        system = AutonomousEmailMarketingSystem()
        system.run()
    except Exception as e:
        logger.error(f"Main system failed: {str(e)}")