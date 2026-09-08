from itertools import combinations

def latex_element(element):
    """Convert a single element to LaTeX."""

    if element == EMPTY_SET:
        return r"\varnothing"

    if isinstance(element, str):
        if element.strip() in {"\\varnothing"}:
            return r"\varnothing"

        replacements = {
            "\\": r"\textbackslash{}",
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            "{": r"\{",
            "}": r"\}",
        }

        result = element
        for old, new in replacements.items():
            result = result.replace(old, new)

        return r"\text{" + result + "}"

    return str(element)


def latex_set(s):
    """Recursively convert a Python set/frozenset into LaTeX."""

    if len(s) == 0:
        return r"\varnothing"

    elements = sorted(s, key=str)

    formatted = []

    for element in elements:

        if isinstance(element, (set, frozenset)):
            formatted.append(latex_set(element))

        elif element == EMPTY_SET:
            formatted.append(r"\varnothing")

        else:
            formatted.append(latex_element(element))

    return r"\{" + r",\, ".join(formatted) + r"\}"


# ---------- Power set ----------

def power_set(s):
    """Return the power set of s as a set of frozensets."""

    elements = list(s)

    return {
        frozenset(combination)
        for r in range(len(elements) + 1)
        for combination in combinations(elements, r)
    }


# ---------- Input ----------

EMPTY_SET = "__EMPTY_SET__"


def parse_element(x):

    x = x.strip()

    if x in {"\\varnothing"}:
        return EMPTY_SET

    try:
        return int(x)
    except ValueError:
        pass

    try:
        return float(x)
    except ValueError:
        pass

    return x


def main():

    print("Power Set Generator")
    print("--------------------")

    raw = input(
        "Enter the elements separated by commas "
        "(example: 2, 5, hello, world):\n> "
    )

    elements = [parse_element(x) for x in raw.split(",")]

    # Remove dopubles
    original_set = frozenset(elements)

    iterations = int(
        input(
            "\nNumber of iterations "
            "(1 = P(A), 2 = P(P(A)), etc.):\n> "
        )
    )

    filename = "powerset.tex"

    if not filename:
        filename = "power_set.tex"

    if not filename.endswith(".tex"):
        filename += ".tex"

    current = original_set

    for i in range(iterations):
        current = power_set(current)

        print(
            f"Iteration {i + 1}: "
            f"{len(current)} elements"
        )

    output = latex_set(current)

    with open(filename, "w", encoding="utf-8") as file:
        file.write(output)

    print(f"\nDone!")
    print(f"Result written to: {filename}")

    if len(output) < 5000:
        print("\nLaTeX output:")
        print(output)
    else:
        print(
            f"\nThe LaTeX output is {len(output):,} characters long."
        )


if __name__ == "__main__":
    main()