import psutil


def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def get_memory_usage():
    return psutil.virtual_memory().percent


def get_disk_usage():
    return psutil.disk_usage("/").percent


def check_status(value, threshold):
    if value >= threshold:
        return "WARNING"

    return "OK"
