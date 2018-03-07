'''
Created on 2017. 12. 22.

@author: jongyeob
'''

import os
import threading

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

import swpy
from swpy import utils2 as utils

from datetime import datetime
from cStringIO import StringIO

FTP_PORT = 8511
TEST_USER = 'swpy'
TEST_PASSWD = 'swpy.passwd'
FTPD = None

def setup_function(function):
    global FTPD
    
    test_dir = swpy.RESOURCE_DIR + '/test/'
 
 
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    authorizer.add_user(TEST_USER, TEST_PASSWD, test_dir, perm='elradfmwM')
    authorizer.add_anonymous(test_dir)

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "pyftpdlib based ftpd ready."

    # Specify a masquerade address and the range of ports to use for
    # passive connections.  Decomment in case you're behind a NAT.
    #handler.masquerade_address = '151.25.42.11'
    #handler.passive_ports = range(60000, 65535)

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = ('', FTP_PORT)
    FTPD = FTPServer(address, handler)

    # set a limit for connections
    FTPD.max_cons = 256
    FTPD.max_cons_per_ip = 5
    
    server_thread = threading.Thread(target=FTPD.serve_forever)       
    server_thread.start()
                

def teardown_function(function):
    FTPD.close_all()
    
    
def test_connect():
    
    url = 'ftp://localhost:{}/'.format(FTP_PORT)
    ftp = swpy.FtpDownloader(url)
    
    ftp.connect(TEST_USER,TEST_PASSWD)
    
    assert ftp.ftp is not None, "FTP Connection Failed. Check URL"
    
    ftp.disconnect()

def test_fetch():
    
    url = 'ftp://localhost:{}/testfile'.format(FTP_PORT)
    ftp = swpy.FtpDownloader(url)
    
    ftp.connect(TEST_USER, TEST_PASSWD)
    
    time_in = datetime.now()
    
    buffer = StringIO()
    ftp.fetch(time_in, buffer)
    
    text = buffer.getvalue()
    
    assert text == '1234567890', 'Diffrent Content'
    
    buffer.close()
    ftp.disconnect()
    
def test_request():
    
    url = 'ftp://localhost:{}/%Y%m%d/%Y%m%d_%H%M%S'.format(FTP_PORT)
    ftp = swpy.FtpDownloader(url)

    ftp.connect(TEST_USER, TEST_PASSWD)
    
    
    test_time = utils2.time_parse("20171220_170122")
    
    request_time = ftp.request(test_time)
    
    assert test_time == request_time, "Not match request time"

    ftp.disconnect()
