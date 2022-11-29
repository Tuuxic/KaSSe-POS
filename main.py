import app
import threading
import sys
import os

if __name__ == '__main__':
    os.chdir(sys.path[0])
    if 'noscan' not in sys.argv:
        import scan
        scan_thread = threading.Thread(target=scan.run, args=(app.send_code,), daemon=True)
        scan_thread.start()
    app.run()
