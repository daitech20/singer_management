# -*- coding: utf-8 -*-


def get_error_code(error_code: int):
    message_error = ERROR_CODE.get(error_code)
    return {
        "success": 0,
        "error": message_error
    }


ERROR_CODE = {

}
