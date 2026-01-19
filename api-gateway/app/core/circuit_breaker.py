import time

class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_time=10):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time

        self.failure_count = 0
        self.state = "CLOSED"  # CLOSED | OPEN | HALF-OPEN
        self.last_failure_time = None

    def allow_request(self) -> bool:
        if self.state == "OPEN":
            elapsed = time.time() - self.last_failure_time
            if elapsed > self.recovery_time:
                self.state = "HALF-OPEN"
                print("Circuit Breaker HALF-OPEN")
                return True
            print("Circuit Breaker OPEN")
            return False
        return True

    def record_success(self):
        self.failure_count = 0
        self.state = "CLOSED"
        print("Circuit Breaker CLOSED")

    def record_failure(self):
        self.failure_count += 1
        print(f"Circuit Breaker failure {self.failure_count}")

        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            self.last_failure_time = time.time()
            print("Circuit Breaker OPENED")

orders_cb = CircuitBreaker(failure_threshold=3, recovery_time=10)
products_cb = CircuitBreaker(failure_threshold=3, recovery_time=10)
