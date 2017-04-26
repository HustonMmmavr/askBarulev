from cgi import parse_qsl
def app(environment, response):

    resp = ['<p>I Like ruby!</p>']
    # resp.append('Post:')
    # resp.append('<form method="post">')
    # resp.append('<input type="text" name = "test">')
    # resp.append('<input type="submit" value="Send">')
    # resp.append('</form>')

    d = parse_qsl(environment['QUERY_STRING'])
    #print(d)
    if environment['REQUEST_METHOD'] == 'POST':
        resp.append('<h1>Post  data:</h1>')
        resp.append(str(environment['wsgi.input'].read(), "utf-8"))

    if environment['REQUEST_METHOD'] == 'GET':
        if environment['QUERY_STRING'] != '':
            resp.append('<h1>Get data:</h1>')
            for ch in d:
                resp.append(' = '.join(ch))
                #print (ch)
                resp.append('<br>')

    resp_len = sum(len(line) for line in resp)
    response('200 OK', [('Content-type', 'text/html'),
                              ('Content-Length', str(resp_len))])

    # xrange
    for i in range(len(resp)):
        resp[i] = bytes(resp[i], "utf-8")
    return resp
