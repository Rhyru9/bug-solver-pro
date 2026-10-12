"""Illustrative retry that resends the same webhook without an idempotency key."""


def deliver(event, http_post):
    http_post(event)
    http_post(event)
