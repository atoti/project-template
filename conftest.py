import os

# Disable atoti telemetry and EULA message before any import of `atoti`.
for name in ["ATOTI_DISABLE_TELEMETRY", "ATOTI_HIDE_EULA_MESSAGE"]:
    # Set the variable using `os.environ` instead of pytest's `MonkeyPatch` so that the change happens before pytest evaluates other modules.
    os.environ[name] = str(True)
