#!/usr/bin/env python
import threading

from pyserverless.apps.message_scheduler import poster
from pyserverless.serverless import app
import codefast as cf

cf.logger.level = "info"


threading.Thread(target=poster).start()
app.run(host='0.0.0.0', port=9000, debug=True)
