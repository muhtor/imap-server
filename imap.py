from pprint import pprint
from imap_tools import MailBox, A, MailMessageFlags
from uuid import uuid4
from imapclient import IMAPClient

port = 993
IMAP_SERVER = 'imap.mail.us-east-1.awsapps.com'  # AWS IMAP server address


class IMAPClientAPi:
    user = 'muhtor@yusufjanov.awsapps.com'
    password = 'pwd'

    def imap_client(self):
        try:
            with IMAPClient(host=IMAP_SERVER) as server:
                server.login(username=self.user, password=self.password)
                select_info = server.select_folder('INBOX')
                print("FOLDERS: ", select_info)
                print('%d messages in INBOX' % select_info[b'EXISTS'])
                print('\n============================')
                # search criteria are passed in a straightforward way
                # (nesting is supported)
                # messages = server.search(['FROM', 'best-friend@domain.com'])
                messages = server.search()
                # fetch selectors are passed as a simple list of strings.
                # response = server.fetch(messages, ['FLAGS', 'RFC822.SIZE'])
                response = server.fetch(messages, ['FLAGS', 'RFC822.SIZE'])
                for msg_id, data in server.fetch(messages, ['ENVELOPE']).items():
                    envelope = data[b'ENVELOPE']
                    print('ID #%d: "%s" received %s' % (msg_id, envelope.subject.decode(), envelope.date))

                # type, data = mail.search(None, '(UNSEEN) (TEXT example)')
                # mail_ids = data[0]
                # id_list = mail_ids.split()
                #
                # for i in reversed(id_list):

                # `response` is keyed by message id and contains parsed,
                # converted response items.
                # for message_id, data in response.items():
                #     # print('{id}: {size} bytes, flags={flags}'.format(
                #     #     id=message_id,
                #     #     size=data[b'RFC822.SIZE'],
                #     #     flags=data[b'FLAGS']))
                #     print("ID...", message_id)
                #     print("data...", data)
        except Exception as e:
            print("Exc.......", e.args)


class MailBoxAPi:
    user = 'muhtor@yusufjanov.awsapps.com'
    password = 'pwd'

    def imap_client(self):
        with MailBox(host=IMAP_SERVER).login(self.user, self.password, 'INBOX') as mailbox:

            print("Connected: ")
            res = []
            # responses = mailbox.idle.wait(timeout=60)
            # if responses:
            for msg in mailbox.fetch(A(seen=False)):
                data = {
                    "ID": msg.uid,
                    "SUBJECT": msg.subject,
                    "TEXT": msg.text,
                    "HTML": msg.html,
                    "FROM": msg.from_values,
                    "TO": msg.to_values,
                    "DATE": msg.date,
                    "ATTACH": None,
                }
                if msg.attachments:
                    for att in msg.attachments:  # list: imap_tools.MailAttachment
                        voice_name = f'voice-{uuid4()}.mp3'
                        with open(f'D:\\PROJECTS\\imap\\voice\\{voice_name}', 'wb') as f:
                            voice = f.write(att.payload)
                            print("V........", voice, type(voice))
                        file = {
                            "filename": att.filename,
                            "content_id": att.content_id,
                            "content_type": att.content_type,
                            "size": att.size,
                            # "body": att.payload,
                        }
                        data['ATTACH'] = file
                mailbox.flag(msg.uid, MailMessageFlags.SEEN, True)
                res.append(data)
            pprint(res)
