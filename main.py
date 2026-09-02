import json
import argparse
from api_monitor import check_api

from health_monitor import (
    get_cpu_usage, 
    get_disk_usage, 
    get_memory_usage,
    check_status
)
from docker_manager import (
    get_container_health,
    get_container_status,
    get_container_logs,
    start_container,
    restart_container,
    wait_for_health
)


def load_config():

    with open("config.json", "r") as file:
        return json.load(file)


def run_health_check(config):
    cpu = get_cpu_usage()
    disk = get_disk_usage()
    memory = get_memory_usage()
    

    print("================================")
    print("       SYSTEM HEALTH")
    print("================================")

    print(
        f"CPU Usage    : {cpu}% "
        f"[{check_status(cpu, config['cpu_threshold'])}]"
    )
        
    print(
        f"Memory Usage : {memory}% "
        f"[{check_status(memory, config['memory_threshold'])}]"
    )
        
    print(
        f"Disk Usage   : {disk}% "
        f"[{check_status(disk, config['disk_threshold'])}]"
    )


def run_api_check(config):

    print("================================")
    print("         API HEALTH")
    print("================================")

    result = check_api(url=config['endpoint_url'])

    print(f"status code: {result['status_code']}")
    print(f"healthy: {result['healthy']}")

    if not result['healthy']:
        print("API health check FAILED")
        return 1

    print("API health check PASSED")
    return 0


def run_docker_check(container):
    status = get_container_status(container)
    health = get_container_health(container)

    print("================================")
    print("       DOCKER STATUS")
    print("================================")

    print(f"Container : {container}")
    print(f"Status    : {status}")
    print(f"Health    : {health}")    


def get_docker_logs(container):
    logs = get_container_logs(container)
    
    print("================================")
    print("       DOCKER LOGS")
    print("================================")

    print(logs)


{
    # def auto_heal(container):
#     print("================================")
#     print("          AUTO HEAL")
#     print("================================")
#     health = get_container_health(container)
#     print(f"Container : {container}")
#     print(f"Health    : {health['stdout']}")
#     if health['stdout'] == "healthy":
#         print()
#         print("Container is healthy.")
#         print("No action required.")
#         return 0
#     print()
#     print("Container is unhealthy.")
#     print("Collecting logs...")
#     logs = get_container_logs(container)
#     print()
#     print("Recent logs:")
#     print(logs)
#     print()
#     print("Restarting container...")
#     restart_container(container)
#     print("Waiting for recovery...")
#     recovered = wait_for_health(container)
#     if recovered:
#         print()
#         print("Container recovered successfully.")
#         return 0
#     print()
#     print("Container failed to recover.")
#     return 1
}


def auto_heal(container):

    print("================================")
    print("          AUTO HEAL")
    print("================================")

    status = get_container_status(container)

    print(f"Container : {container}")
    print(f"Status    : {status}")

    if status != "running":

        print()
        print("Container is not running.")
        print("Starting container...")

        start_container(container)

        print("Waiting for recovery...")

        recovered = wait_for_health(container)

        if recovered:

            print()
            print("Container started successfully.")

            return 0

        print()
        print("Container failed to become healthy.")

        return 1

    health = get_container_health(container)

    print(f"Health    : {health}")

    if health == "healthy":

        print()
        print("Container is healthy.")
        print("No action required.")

        return 0

    print()
    print("Container is unhealthy.")
    print("Collecting logs...")

    logs = get_container_logs(container)

    print()
    print("Recent logs:")
    print(logs)

    print()
    print("Restarting container...")

    restart_container(container)

    print("Waiting for recovery...")

    recovered = wait_for_health(container)

    if recovered:

        print()
        print("Container recovered successfully.")

        return 0

    print()
    print("Container failed to recover.")

    return 1


def main():

    config = load_config()
    
    parser = argparse.ArgumentParser(
        description="DevOps Health Monitor"
    )

    parser.add_argument(
        "command",
        choices=["health", "api", "docker-status", "docker-logs", "auto-heal"],
        help="Command to execute"
    )

    args = parser.parse_args()

    if args.command == "health":
        print("Running system health check...")
        run_health_check(config=config)

    elif args.command == "api":
        print("Running API health check...")
        run_api_check(config=config)

    elif args.command == "docker-status":

        run_docker_check(container=config['container'])

    elif args.command == "docker-logs":

        get_docker_logs(container=config['container'])

    elif args.command == "auto-heal":

        return auto_heal(container=config['container'])
        
        

if __name__ == "__main__":
    exit(main())

