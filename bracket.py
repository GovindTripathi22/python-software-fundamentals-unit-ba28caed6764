def validate_bracket(lines):
    problems = []
    match_counts = {}
    winners = []

    for number, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip("\r\n")
        text = line.strip()
        if text == "":
            continue

        if text.startswith("Winner:"):
            winners.append(text[len("Winner:"):].strip())
            continue

        if line.count(" vs ") != 1:
            problems.append("line " + str(number) + "needs exactly one ' vs '")
            continue

        left, right = line.split(" vs ")
        left = left.strip()
        right = right.strip()

     
        if left == "" or right == "":
            problems.append("Line " + str(number) + " is missing a player name")
            continue

        if left == right:
            problems.append(left + " is listed against herself")
            players = [left]
        else:
            players = [left, right]
                ##