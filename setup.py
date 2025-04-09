from setuptools import setup

setup(
    name="cperms_ins_enc",
    version="1.0",
    description="A module for enumerating Cayley permutations using the insertion encoding.",
    author="Abigail Ollson",
    author_email="a.n.ollson@keele.ac.uk",
    packages=[
        "cayley_permutations",
        "gridded_cayley_permutations",
        "vertical_insertion_encoding",
        "horizontal_ins_enc",
        "tilescope",
        "vatters_method",
    ],
    description="Enumerate Cayley permutations using the insertion encoding.",
    keywords="enumerative combinatorics pattern avoidance cayley permutations insertion encoding",
    install_requires=[
        "typing",
        "comb_spec_searcher",
    ],  # external packages as dependencies
)
