def get_backoff_delay(retries: int) -> int:
    return 30 * (2 ** retries)