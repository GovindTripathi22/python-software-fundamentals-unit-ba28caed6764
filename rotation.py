NO_PLAN = "No valid session to plan."


def read_count(text):
    text = text.strip()
    if text.isdecimal():
        return int(text)
    return 0


def build_plan(lanes, legs, swimmers):
    slots = list(swimmers)
    while len(slots) < lanes:
        slots.append(None)
    plan = []
    for leg in range(legs):
        shift = leg % len(slots)
        order = slots[shift:] + slots[:shift]
        plan.append((order[:lanes], order[lanes:]))
    return plan


def format_plan(plan):
    lines = []
    leg_number = 1
    for in_lanes, waiting in plan:
        if leg_number > 1:
            lines.append("")
        lines.append("Leg " + str(leg_number))
        lane_number = 1
        for name in in_lanes:
            if name is None:
                name = "empty"
            lines.append("  Lane " + str(lane_number) + ": " + name)
            lane_number = lane_number + 1
        if len(waiting) > 0:
            lines.append("  Waiting: " + ", ".join(waiting))
        leg_number = leg_number + 1
    return "\n".join(lines)


def main():
    print("Enter lanes, legs, then swimmer names (blank line or done to finish):")
    lanes = read_count(input())
    if lanes == 0:
        print(NO_PLAN)
        return
    legs = read_count(input())
    if legs == 0:
        print(NO_PLAN)
        return
    swimmers = []
    name = input().strip()
    while name != "" and name.lower() != "done":
        swimmers.append(name)
        name = input().strip()
    if len(swimmers) == 0:
        print(NO_PLAN)
        return
    print(format_plan(build_plan(lanes, legs, swimmers)))


if __name__ == "__main__":
    main()