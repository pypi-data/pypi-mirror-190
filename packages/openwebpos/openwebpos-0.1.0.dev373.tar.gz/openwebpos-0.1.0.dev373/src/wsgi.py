from dotenv import load_dotenv

from openwebpos import create_app

load_dotenv()

application = create_app()

if __name__ == '__main__':
    try:
        application.run()
    except RecursionError as re:
        print("Unable to start OpenWebPOS. Please check your configuration.")
        print("Error/s:" + str(re))
