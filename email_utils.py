import imaplib
import email
from bs4 import BeautifulSoup


class Email_Logger():

    def __init__(self, info) -> None:
        self.email = info["generic_info"]["email"]
        self.password = info["generic_info"]["pass"]
        self.server = 'imap.gmail.com'
        self.mail = None
        self.last_mail = ""

    def login(self):

        self.mail = imaplib.IMAP4_SSL(self.server)
        self.mail.login(self.email, self.password)

    def get_last_msg(self, sender="'noreply@visametric.com'"):
        self.mail.select('inbox')
        status, data = self.mail.search(
            None, f"(FROM {sender})")
        mail_ids = []

        for block in data:
            mail_ids += block.split()

        mail_ids = [mail_ids[-1]]
        for i in mail_ids:

            status, data = self.mail.fetch(i, '(RFC822)')

            for response_part in data:
                if isinstance(response_part, tuple):
                    message = email.message_from_bytes(response_part[1])
                    # mail_from = message['from']
                    # mail_subject = message['subject']
                    # if message.is_multipart():
                    #     mail_content = ''
                    #     for part in message.get_payload():

                    #         if part.get_content_type() == 'text/plain':

                    #             mail_content += part.get_payload()
                    # else:
                    #     mail_content = message.get_payload()

                    mail_content = message.get_payload()
                    self.last_mail = mail_content
                    return {"content": mail_content, "date": message["date"]}

    def find_code(self):
        soup = BeautifulSoup(self.last_mail, "html.parser")
        code_element = soup.find_all(
            "h2")[-1]
        code = str(code_element.encode_contents().decode("utf-8").strip())
        return code
