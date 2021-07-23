"""
galmsps.py

Copyright (c) 2021 Ujjwal Panda

Script to scrap the database of all galactic millisecond pulsars. The database
was created by Duncan Lorimer and is now maintained by Elizabeth Ferrera. The
data is available as a text file, which this script scraps and parses using the
art of regular expressions. After the data has been stored as JSON, I have used
the dataset package to store the data as an SQLite database. Thanks to dataset,
the code that constructs the database is just 4 lines long.
"""

if __name__ == "__main__":

    import re
    import dataset  # type: ignore

    from json import dump
    from pathlib import Path
    from requests import get

    numeric = (
        lambda _: float(_)
        if re.search(re.compile(r"^[-+]?[0-9]*[.]?[0-9]+([eE][-+]?[0-9]+)?$"), _)
        else None
    )

    data = {
        str(i + 1): {
            key: conv(value)  # type: ignore
            for (key, conv), value in zip(
                [
                    ("NAME", str),
                    ("P0", numeric),
                    ("DM", numeric),
                    ("GL", numeric),
                    ("GB", numeric),
                    ("PB", numeric),
                    ("A1", numeric),
                    ("DISCOVERY YEAR", int),
                    ("NOTES", str),
                ],
                values,
            )
        }
        for i, values in enumerate(
            [
                [_ for _ in re.split(r"\s+", _) if _]
                for _ in re.split(
                    r"\n+",
                    re.sub(
                        re.compile(r"^([^#]*)[#](.*)$", re.MULTILINE),
                        "",
                        get(
                            "http://astro.phys.wvu.edu/GalacticMSPs/GalacticMSPs.txt"
                        ).content.decode(),
                    ).strip(),
                )
            ]
        )
    }

    with open("galmsps.json", "w+") as fobj:
        dump(
            obj=dict(data=data),
            fp=fobj,
            indent=4,
        )

    dbpath = Path.cwd().joinpath("galmsps.db")
    dbpath.unlink(missing_ok=True)

    db = dataset.connect(f"sqlite:///{dbpath}")
    table = db["data"]
    for item in data.values():
        table.insert(item)
    db.close()