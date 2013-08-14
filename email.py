# import the mandrill library
import mandrill

# import our local settings
import local_settings


class Email:
    """
    Methods for sending user emails and interacting with the Mandrill API.

    """
    def __init__(self):
        """
        Initialize the Mandrill connection.

        """
        self.mandrill_client = mandrill.Mandrill(local_settings.MANDRILL_API_KEY)

    def send_ping(self):
        """
        Ping the Mandrill API to ensure everything is properly set up.
        Returns a "PONG!" when successful.

        """

        print(self.mandrill_client.users.ping())

    def send_email(self, html, subject, from_email, to_email, to_name):
        """
        Send an email using Mandrill, and catch/return any exceptions.

        """

        # roll up the message object
        message = {
            'html': html,
            'subject': subject,
            'from_email': from_email,
            'to': [
                {
                    'email': to_email,
                    'name': to_email
                }
            ],
        }

        try:
            # try to send an email in an async fashion
            result = self.mandrill_client.messages.send(
                message=message,
                async=True
            )
        except Exception as exception:
            # catch and return the exception
            result = exception

        return result
