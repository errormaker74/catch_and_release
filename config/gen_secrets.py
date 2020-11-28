import json
from pathlib import Path

from django.core.management.utils import get_random_secret_key


def main() -> None:
    base_dir = Path(__file__).resolve().parent.parent
    secrets = {
        'SECRET_KEY': get_random_secret_key(),
        'SLACK_TOKEN': '',
        'SLACK_CHANNEL': '',
        'STREAMING_URL': '',
    }
    with open(base_dir / 'secrets.json', mode='w') as f:
        json.dump(secrets, f, indent=2)


if __name__ == '__main__':
    main()
