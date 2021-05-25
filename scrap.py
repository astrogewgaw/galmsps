if __name__ == "__main__":

    import re

    from json import dump
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
