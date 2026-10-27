import os
import subprocess
import sys
import unittest
####
from rotation import NO_PLAN, build_plan, format_plan, read_count

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rotation.py")


def run_program(lines):
    typed = "\n".join(lines) + "\n"
    result = subprocess.run([sys.executable, SCRIPT], input=typed,
                            capture_output=True, text=True)
    return result.stdout


class BuildPlanTests(unittest.TestCase):
    def test_three_lanes_two_legs_matches_example(self):
        plan = build_plan(3, 2, ["Ana", "Ben", "Cid"])
        self.assertEqual(plan[0], (["Ana", "Ben", "Cid"], []))
        self.assertEqual(plan[1], (["Ben", "Cid", "Ana"], []))

    def test_nobody_keeps_the_same_lane_on_the_next_leg(self):
        cases = [(3, 4, ["Ana", "Ben", "Cid"]),
                 (2, 5, ["Ana", "Ben", "Cid", "Dee", "Eve"]),
                 (4, 6, ["Ana", "Ben"]),
                 (3, 3, ["Ana"])]
        for lanes, legs, swimmers in cases:
            plan = build_plan(lanes, legs, swimmers)
            for leg in range(1, legs):
                before = plan[leg - 1][0]
                after = plan[leg][0]
                for lane in range(lanes):
                    if after[lane] is not None:
                        self.assertNotEqual(before[lane], after[lane])

    def test_extras_wait_and_appearances_add_up(self):
        swimmers = ["Ana", "Ben", "Cid", "Dee", "Eve"]
        plan = build_plan(2, 3, swimmers)
        total = 0
        for in_lanes, waiting in plan:
            self.assertEqual(len(in_lanes), 2)
            self.assertEqual(len(waiting), 3)
            self.assertEqual(sorted(in_lanes + waiting), sorted(swimmers))
            total = total + len(in_lanes) + len(waiting)
        self.assertEqual(total, len(swimmers) * 3)

    def test_spare_lanes_are_empty(self):
        plan = build_plan(4, 1, ["Ana", "Ben"])
        self.assertEqual(plan[0], (["Ana", "Ben", None, None], []))


class FormatAndCountTests(unittest.TestCase):
    def test_format_numbers_legs_and_lanes_from_one(self):
        text = format_plan(build_plan(3, 2, ["Ana", "Ben"]))
        self.assertEqual(text, "Leg 1\n"
                               "  Lane 1: Ana\n"
                               "  Lane 2: Ben\n"
                               "  Lane 3: empty\n"
                               "\n"
                               "Leg 2\n"
                               "  Lane 1: Ben\n"
                               "  Lane 2: empty\n"
                               "  Lane 3: Ana")

    def test_format_shows_waiting_list(self):
        text = format_plan(build_plan(1, 1, ["Ana", "Ben", "Cid"]))
        self.assertEqual(text, "Leg 1\n  Lane 1: Ana\n  Waiting: Ben, Cid")

    def test_read_count(self):
        self.assertEqual(read_count("3"), 3)
        self.assertEqual(read_count(" 4\r"), 4)
        self.assertEqual(read_count("0"), 0)
        self.assertEqual(read_count("-2"), 0)
        self.assertEqual(read_count("three"), 0)
        self.assertEqual(read_count(""), 0)


class ProgramTests(unittest.TestCase):
    def test_full_run(self):
        out = run_program(["3", "2", "Ana", "Ben", "Cid", "done"])
        self.assertIn("Leg 1\n  Lane 1: Ana\n  Lane 2: Ben\n  Lane 3: Cid\n", out)
        self.assertIn("Leg 2\n  Lane 1: Ben\n  Lane 2: Cid\n  Lane 3: Ana\n", out)

    def test_blank_line_ends_names(self):
        out = run_program(["2", "1", "Ana", "", "Ben"])
        self.assertIn("Lane 1: Ana\n  Lane 2: empty\n", out)
        self.assertNotIn("Ben", out)

    def test_zero_lanes(self):
        out = run_program(["0", "2", "Ana", "done"])
        self.assertEqual(out.splitlines()[-1], NO_PLAN)
        self.assertNotIn("Leg", out)

    def test_zero_legs(self):
        out = run_program(["3", "0", "Ana", "done"])
        self.assertEqual(out.splitlines()[-1], NO_PLAN)

    def test_done_before_any_name(self):
        out = run_program(["3", "2", "done"])
        self.assertEqual(out.splitlines()[-1], NO_PLAN)
        self.assertNotIn("Leg", out)


if __name__ == "__main__":
    unittest.main()