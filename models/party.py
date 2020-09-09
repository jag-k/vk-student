import math

PLAN_ADMIN = -1
PLAN_FREE = 0
PLAN_EXTENDED = 1
PLAN_PREMIUM = 2

REQUEST_LIMITS = {  # TODO: move to some config?
    PLAN_ADMIN: math.inf,
    PLAN_FREE: 60,
    PLAN_EXTENDED: 300,
    PLAN_PREMIUM: 700
}

USAGE_LIMITS = {
    PLAN_ADMIN: math.inf,
    PLAN_FREE: 3000,
    PLAN_EXTENDED: 12000,
    PLAN_PREMIUM: 40000
}


class Party:
    def __init__(self, name, plan, request_count=0, usage=0):
        self.name = name
        self.plan = plan
        self.request_count = request_count
        self.usage = usage

    @staticmethod
    def from_dict(orig):
        return Party(
            orig["name"],
            orig["plan"],
            orig["request_count"],
            orig["usage"]
        )

    def to_dict(self):
        return {
            "name": self.name,
            "plan": self.plan,
            "request_count": self.request_count,
            "usage": self.usage
        }

    @property
    def is_something_reached(self):
        return self.is_request_limit_reached or self.is_usage_limit_reached

    @property
    def is_request_limit_reached(self):
        return self.request_count > self.request_limit

    @property
    def is_usage_limit_reached(self):
        return self.usage > self.usage_limit

    @property
    def request_limit(self):
        return REQUEST_LIMITS[self.plan]

    @property
    def usage_limit(self):
        return USAGE_LIMITS[self.plan]
