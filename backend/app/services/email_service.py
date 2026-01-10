
import logging

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_approval_email(email: str, name: str, branch_name: str):
        """Mock sending an approval email."""
        msg = f"SENT APPROVAL EMAIL to {email}: Welcome {name}! Your account has been approved and assigned to branch: {branch_name}."
        print(msg)
        logger.info(msg)

    @staticmethod
    def send_rejection_email(email: str, name: str, reason: str):
        """Mock sending a rejection email."""
        msg = f"SENT REJECTION EMAIL to {email}: Hello {name}. Unfortunately, your registration was rejected for the following reason: {reason}."
        print(msg)
        logger.info(msg)

email_service = EmailService()
