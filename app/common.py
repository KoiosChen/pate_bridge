def success_return(data="", message=""):
    return {"code": "success", "data": data, "message": message}


def false_return(data="", message=""):
    return {"code": "false", "data": data, "message": message}
