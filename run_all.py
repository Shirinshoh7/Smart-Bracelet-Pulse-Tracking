import threading
import os

def run_flask():
    os.system("python app.py")

def run_bot():
    os.system("python bot.py")

if __name__ == "__main__":
    t1 = threading.Thread(target=run_flask)
    t2 = threading.Thread(target=run_bot)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
