import time, random, constants, subprocess
from pathlib import Path

def main():
    configs_path = Path("configs")
    config_files = sorted(configs_path.glob('*_config.py'))

    for config_file in config_files:
        print(f"Starting LinkedIn application with configuration: {config_file.name}")
        # Copy the current config file to config.py
        subprocess.run(["cp", "-f", str(config_file), "config.py"], check=True)

        # Run the LinkedIn application
        subprocess.run(["python3", "linkedin.py"], check=True)

        # Wait for a specified number of seconds or implement a random wait time
        sleep_time = random.uniform(constants.botSleepInBetweenSearchesBottom, constants.botSleepInBetweenSearchesTop)
        print(f"Sleeping for {sleep_time} seconds.")
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
