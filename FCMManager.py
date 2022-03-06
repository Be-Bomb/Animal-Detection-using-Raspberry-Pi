# import firebase_admin
# from pyfcm import FCMNotification
from firebase_admin import credentials, messaging

# cred = credentials.Certificate("service-account-file.json")
# firebase_admin.initialize_app(cred)


def sendPush(title, msg, registration_token, dataObject=None):

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=msg,
        ),
        data=dataObject,
        token=registration_token[0],
    )

    response = messaging.send(message)
    
    print("Succesfully sent message:", response)