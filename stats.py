

def on_request_success(request_type, name, response_time, response_length):
    global_stats.log_request(request_type, name, response_time, response_length)

def on_request_failure(request_type, name, response_time, exception):
    global_stats.log_error(request_type, name, exception)