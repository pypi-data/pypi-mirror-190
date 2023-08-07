import os

import boto3
from botocore.exceptions import ClientError
from pinpoint.exception import PinPointException, ErrorCodes


class MailService:
    region = "eu-central-1"
    channel_type = "EMAIL"
    applicationId = None
    aws_access_key_id = None
    aws_secret_access_key = None
    address_dict = dict()
    message_configuration = dict()
    template_configuration = dict()
    message_request = dict()
    response = None
    destinationAddresses = None
    message = None

    def __init__(self, region='eu-central-1', channel_type='EMAIL',
                 applicationId=None, aws_access=None, aws_secret=None):
        self.region = os.environ.get('REGION', region)
        self.applicationId = os.environ.get('PINPOINT_APPLICATION_ID', applicationId)
        if self.applicationId is None:
            raise ValueError(ErrorCodes.APPLICATION_ID_ERROR)
        self.aws_access_key_id = os.environ.get('AWS_ACCESS', aws_access)
        if self.aws_access_key_id is None:
            raise ValueError(ErrorCodes.AWS_ACCESS_KEY_ERROR)
        self.aws_secret_access_key = os.environ.get('AWS_SECRET', aws_secret)
        if self.aws_secret_access_key is None:
            raise ValueError(ErrorCodes.AWS_SECRET_KEY_ERROR)
        self.channel_type = os.environ.get('CHANNEL_TYPE', channel_type)
        self.is_mail_send = False
        self.error_message = ErrorCodes.MAIL_SEND_ERROR
        self.client = boto3.client('pinpoint', region_name=self.region, aws_access_key_id=self.aws_access_key_id,
                                   aws_secret_access_key=self.aws_secret_access_key)

    def send(self, sender, to_addresses, message=None, template_name=None, template_version=None):
        try:
            self.destinationAddresses = to_addresses
            if self.destinationAddresses is None:
                raise ValueError(ErrorCodes.DESTINATION_ADDRESS_ERROR)
            self.message = message
            if self.message is None:
                raise ValueError(ErrorCodes.MESSAGE_ERROR)

            self.address_dict = {
                to_address: {
                    'ChannelType': 'EMAIL'
                } for to_address in to_addresses
            }
            self.message_configuration = {'EmailMessage': {'FromAddress': sender}}
            self.template_configuration = {
                'EmailTemplate': {
                    'Name': template_name,
                    'Version': template_version
                }
            }
            self.message_request = {'Addresses': self.address_dict, 'MessageConfiguration': self.message_configuration,
                                    'TemplateConfiguration': self.template_configuration}
            self.response = self.client.send_messages(ApplicationId=self.applicationId,
                                                      MessageRequest=self.message_request)

            self.is_mail_send = self.check_mail_status()
            if self.is_mail_send is False:
                raise PinPointException(self.error_message)
        except ClientError as e:
            raise PinPointException(e.response['Error']['Message'])

    def check_mail_status(self):
        return {
            to_address: message['MessageId'] for
            to_address, message in self.response['MessageResponse']['Result'].items()
        }
