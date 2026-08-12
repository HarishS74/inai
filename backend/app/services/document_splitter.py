SECTIONS = [
    "Coverage",
    "Benefits",
    "Exclusions",
    "Waiting Period",
    "Claims",
    "Claim Procedure",
    "Cashless",
    "Hospital Network",
    "Room Rent",
    "ICU",
    "Co-payment",
    "Sub Limit",
    "Restore Benefit",
    "No Claim Bonus",
    "Day Care",
    "Organ Donor",
    "Ambulance",
    "Pre Hospitalization",
    "Post Hospitalization",
    "Helpline",
    "Customer Care",
    "Contact",
]

MAX_LINES_PER_SECTION = 60
MAX_TOTAL_LINES = 400


def split_sections(text: str):

    lines = text.splitlines()

    extracted = []
    total = 0

    i = 0

    while i < len(lines):

        line = lines[i].strip()

        if any(h.lower() in line.lower() for h in SECTIONS):

            extracted.append(line)
            total += 1

            for j in range(i + 1, min(i + MAX_LINES_PER_SECTION, len(lines))):

                l = lines[j].strip()

                if not l:
                    continue

                extracted.append(l)
                total += 1

                if total >= MAX_TOTAL_LINES:
                    return "\n".join(extracted)

            i += MAX_LINES_PER_SECTION

        i += 1

    return "\n".join(extracted)