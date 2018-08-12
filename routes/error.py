def error(request, code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    # 不要用数字来作为字典的 key
    # 但是在 HTTP 协议中 state code 都是数字， 用数字似乎更方便所以打破了这个原则
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')