from datetime import datetime
def write_to_logs(domain_name):
    with open("logs.txt", "a") as logs:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        time = datetime.strftime(datetime.now(), "%H.%M.%S")
        logs.write("{} {} {}\n".format(date,time, domain_name))

