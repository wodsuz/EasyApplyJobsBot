import sys, time, random, constants, subprocess
from pathlib import Path

def main(base_path):
    configs_path = Path(f"{base_path}/configs")
    config_files = sorted(configs_path.glob('*_config.py'))

    for config_file in config_files:
        print(f"Starting LinkedIn application with configuration: {config_file.name}")
        # Copy the current config file to config.py
        subprocess.run(["cp", "-f", str(config_file), f"{base_path}/config.py"], check=True)

        # Run the LinkedIn Easy Apply bot
        subprocess.run(["python", f"{base_path}/runner.py"], check=True)

        # Wait for a specified number of seconds or implement a random wait time
        sleep_time = random.uniform(constants.botSleepInBetweenSearchesBottom, constants.botSleepInBetweenSearchesTop)
        print(f"Sleeping for {sleep_time} seconds.")
        time.sleep(sleep_time)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python allConfigsRunner.py <base_path>")
        sys.exit(1)
    main(sys.argv[1])
