import re
import json
import requests

from schema import Use, Schema  # type: ignore


# URL of the galactic MSPs catalog.
url = "http://astro.phys.wvu.edu/GalacticMSPs/GalacticMSPs.txt"

# A regular expression to match comments.
# This is used to remove the comments at
# the beginning of the database.
comment = re.compile(
    r"""
    ^       # Beginning of line.
    ([^#]*) # Do not match zero or more hash characters.
            # This takes care of not matching lines that
            # start with multiple hash characters.
    [#]     # The hash character.
    (.*)    # Match zero or more instances of any character.
    $       # End of line.
    """,
    re.VERBOSE | re.MULTILINE,
)


# A regular expression to match any floating point number,
# such as "9", "9.0", "+8.67" or "-0.67". The number can
# also be in scientific notation ("1e-9").
fpnex = re.compile(
    r"""
    ^                   # Beginning of string.
    [-+]?               # Match zero or more instances of a plus/minus sign.
    [0-9]*              # Match zero or more instances of a numeric character.
    [.]?                # Match zero or more instances of a decimal point.
    [0-9]+              # Match one or more instances of a numeric character.
    ([eE][-+]?[0-9]+)?  # Match an exponent, as in "1e-9".
                        # This pattern matches a sign too,
                        # if present.
    $                   # End of string.
    """,
    re.VERBOSE,
)

# A simple function to deal with numeric values that could possibly be NULL.
isnull = lambda x: float(x) if re.search(fpnex, x) else None

# The key-value map for the database.
kvs = {
    "NAME": Use(str),
    "P": Use(isnull),
    "DM": Use(isnull),
    "GAL_L": Use(isnull),
    "GAL_B": Use(isnull),
    "PBIN": Use(isnull),
    "PSMA": Use(isnull),
    "YEAR": Use(int),
    "NOTES": Use(str),
}


def scrap() -> None:

    """
    Scrap the galactic MSPs database and serialise it to a JSON file.
    """

    cat = requests.get(url)
    text = cat.content.decode()
    data = re.sub(comment, "", text).strip()
    rows = [[_ for _ in re.split(r"\s+", _) if _] for _ in re.split(r"\n+", data)]
    mspp = lambda keys, vals: {key: val for key, val in zip(keys, vals)}
    galmsps = {
        str(i + 1): Schema(kvs).validate(mspp(kvs.keys(), row))
        for i, row in enumerate(rows)
    }

    with open("galmsps.json", "w+") as fobj:
        json.dump(
            galmsps,
            fobj,
            indent=4,
        )


if __name__ == "__main__":

    scrap()