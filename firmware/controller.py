"""Hardware-independent state machine. All durations are bounded; time is wrap-safe."""
try:
    from time import ticks_ms, ticks_diff
except ImportError:
    from time import monotonic
    def ticks_ms(): return int(monotonic() * 1000)
    def ticks_diff(a, b): return a - b


def integer(value, low, high, name):
    if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
        raise ValueError('%s must be an integer from %d to %d' % (name, low, high))
    return value


class Controller:
    def __init__(self, servo, motor, clock=ticks_ms, diff=ticks_diff):
        self.servo, self.motor, self.clock, self.diff = servo, motor, clock, diff
        self.closed_us, self.open_us = 1500, 1000
        self.motor_ready = False
        self.armed_at = None
        self.dose_at = None
        self.duration_ms, self.duty = 0, 0
        self.stop()

    def stop(self):
        self.motor.duty_u16(0)
        self.servo.duty_ns(self.closed_us * 1000)
        self.dose_at = None
        self.armed_at = None

    def configure(self, closed_us=1500, open_us=1000, motor_ready=False):
        closed = integer(closed_us, 700, 2300, 'closed_us')
        opened = integer(open_us, 700, 2300, 'open_us')
        if not isinstance(motor_ready, bool): raise ValueError('motor_ready must be true or false')
        self.stop()
        self.closed_us, self.open_us = closed, opened
        self.motor_ready = motor_ready
        self.servo.duty_ns(closed * 1000)

    def center(self):
        self.stop()
        self.servo.duty_ns(1500000)

    def calibrate(self, pulse_us):
        pulse = integer(pulse_us, 700, 2300, 'pulse_us')
        self.stop()
        self.servo.duty_ns(pulse * 1000)

    def arm(self):
        self.stop()
        self.armed_at = self.clock()

    def dose(self, duration_ms, duty):
        duration = integer(duration_ms, 100, 5000, 'duration_ms')
        duty = integer(duty, 0, 100, 'duty')
        self.tick()
        if self.armed_at is None: raise ValueError('Arm before dispensing; arming expires after 60 seconds')
        if self.dose_at is not None: raise ValueError('A dose is already running')
        if duty and not self.motor_ready: raise ValueError('Verify the module input and enable motor_ready first; duty 0 tests the gate only')
        self.duration_ms, self.duty = duration, duty
        self.dose_at = self.clock()
        self.servo.duty_ns(self.open_us * 1000)
        self.motor.duty_u16(65535 if duty else 0)

    def tick(self):
        now = self.clock()
        if self.armed_at is not None and self.diff(now, self.armed_at) >= 60000:
            self.stop()
        elif self.dose_at is not None:
            elapsed = self.diff(now, self.dose_at)
            if elapsed >= self.duration_ms: self.stop()
            elif elapsed >= 50: self.motor.duty_u16(self.duty * 65535 // 100)

    def status(self):
        self.tick()
        return dict(armed=self.armed_at is not None, dispensing=self.dose_at is not None,
                    motor_ready=self.motor_ready, closed_us=self.closed_us, open_us=self.open_us)
