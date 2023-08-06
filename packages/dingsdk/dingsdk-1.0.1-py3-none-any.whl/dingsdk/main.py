from .chatbots import Chatbot
from .contacts import Contacts
from .persons import Personnel
from .access_token import AccessToken
from .approval import Approval, InstanceCleaner


class DingSDK(AccessToken, Approval, Chatbot, Contacts, Personnel):
    ...
