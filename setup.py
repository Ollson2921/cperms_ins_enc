from setuptools import setup

setup(
    name="cperms_ins_enc",
    version="1.0.0",
    description="A module for enumerating Cayley permutations using the insertion encoding.",
    author="Abigail Ollson",
    author_email="a.n.ollson@keele.ac.uk",
    packages=[
        "cperms_ins_enc",
    ],
    keywords="enumerative combinatorics pattern avoidance cayley permutations insertion encoding",
    install_requires=[
        "comb_spec_searcher",
    ],
)
