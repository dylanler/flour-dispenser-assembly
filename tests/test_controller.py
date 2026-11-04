import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'firmware'))
from controller import Controller


class PWM:
    def duty_u16(self, v): self.duty = v
    def duty_ns(self, v): self.pulse = v


class ControlTests(unittest.TestCase):
    def setUp(self):
        self.now = 0
        self.servo, self.motor = PWM(), PWM()
        self.c = Controller(self.servo, self.motor, lambda: self.now)

    def test_boot_and_unverified_motor(self):
        self.assertFalse(self.c.status()['armed'])
        self.assertEqual(self.motor.duty, 0)
        self.c.arm()
        with self.assertRaises(ValueError): self.c.dose(500, 50)
        self.assertEqual(self.servo.pulse, 1500000)

    def test_startup_kick_and_deadline(self):
        self.c.configure(motor_ready=True)
        self.c.arm(); self.c.dose(500, 25)
        self.assertEqual(self.motor.duty, 65535)
        self.now = 50; self.c.tick()
        self.assertEqual(self.motor.duty, 16383)
        self.now = 500; self.c.tick()
        self.assertEqual(self.motor.duty, 0)
        self.assertEqual(self.servo.pulse, 1500000)
        self.assertFalse(self.c.status()['armed'])

    def test_arm_expiry_and_duplicate(self):
        self.c.arm(); self.c.dose(500, 0)
        with self.assertRaises(ValueError): self.c.dose(500, 0)
        self.c.stop(); self.c.arm(); self.now = 60000
        with self.assertRaises(ValueError): self.c.dose(500, 0)

    def test_invalid_dose_cannot_move_gate(self):
        self.c.arm()
        for duration, duty in [(0,0), (5001,0), (500,-1), (500,101), (True,0), (500,2.5)]:
            with self.assertRaises(ValueError): self.c.dose(duration, duty)
        self.assertEqual(self.servo.pulse, 1500000)

    def test_stop_calibration_and_config_validation(self):
        self.c.calibrate(1400)
        self.assertEqual(self.servo.pulse, 1400000)
        self.c.stop(); self.assertEqual(self.servo.pulse, 1500000)
        with self.assertRaises(ValueError): self.c.configure(closed_us=0)
        with self.assertRaises(ValueError): self.c.configure(motor_ready='yes')


if __name__ == '__main__': unittest.main()
