from pathlib import Path

from summ import Pipeline, Summ
from summ.cli import CLI
from summ.splitter.otter import OtterSplitter


def summ_and_pipe():
    summ = Summ(index="cronutt-facts")

    path = Path(__file__).parent.parent / "interviews"
    pipe = Pipeline.default(path, summ.index)
    pipe.splitter = OtterSplitter(
        speakers_to_exclude=[
            "Cindy Buckmaster",
            "Michelle Greenfield",
            "Vivica",
            "Deanna",
        ]
    )

    return summ, pipe


def main():
    summ, pipe = summ_and_pipe()
    CLI.run(summ, pipe)


if __name__ == "__main__":
    main()
