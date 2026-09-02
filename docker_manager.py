import subprocess
import time

def run_docker_command(command):
    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip()) 

    output = str(result.stdout.strip()) + result.stderr.strip()
    return output


def get_container_status(container_name):

    return run_docker_command(
        [
            "docker",
            "inspect",
            "--format={{.State.Status}}",
            container_name
        ]
    )

def get_container_health(container_name):

    return run_docker_command(
        [
            "docker",
            "inspect",
            "--format={{.State.Health.Status}}",
            container_name
        ]
    )

def get_container_logs(container_name):

    return run_docker_command(
        [
            "docker",
            "logs",
            "--tail",
            "2",
            container_name
        ]
    )

def stop_container(container_name):

    return run_docker_command(
        [
            "docker",
            "stop",
            container_name
        ]
    )

def start_container(container_name):

    return run_docker_command(
        [
            "docker",
            "start",
            container_name
        ]
    )

def restart_container(container_name):

    return run_docker_command(
        [
            "docker",
            "restart",
            container_name
        ]
    )

def wait_for_health(container_name, attempts=10, delay=3):

    for attempt in range(attempts):

        health = get_container_health(container_name)

        print(
            f"Health check {attempt + 1}/{attempts}: "
            f"{health}"
        )

        if health == "healthy":
            return True

        time.sleep(delay)

    return False



if __name__ == "__main__":

    container = "map-api"

    print("Container Status:")
    print(get_container_status(container))

    print()

    print("Container Health:")
    print(get_container_health(container))

    print()

    print("Container Logs:")
    print(get_container_logs(container))