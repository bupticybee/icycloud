from flask import Flask
from flask import make_response
import MySQLdb
import traceback

app = Flask(__name__)


def get_ip_from_address(address):
    db = MySQLdb.connect("localhost","cloud","cloud","icycloud" )
    cursor = db.cursor()
    cursor.execute("select machineip from webui_router where url='%s'" % address)
    rs = cursor.fetchall()
    ip = rs[0][0]
    cursor.close()
    db.close()
    print ip
    return str(ip)

@app.route('/auth/<address>')
def get_route(address):
    print address
    # check address
    for i in address:
	if i not in 'abcdefghijklmnopqrstuvwxyz-0123456789.':
	    return 
    # get the ip
    try:
	ip = get_ip_from_address(address)
    except:
	traceback.print_exc()

    resp = make_response('',200)
    resp.headers['url'] = 'http://' + ip
    print 'success'

    return resp

if __name__ == '__main__':
    app.run(host='127.0.0.1',port='8800')
    #app.run(debug=True)

