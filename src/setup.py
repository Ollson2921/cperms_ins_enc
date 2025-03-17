from setuptools import setup

setup(
    name="cayley_perms_ins_enc",
    version="1.0",
    description="A module for enumerating Cayley permutations using the insertion encoding.",
    #    author='',
    #    author_email='foomail@foo.example',
    packages=[
        "cayley_permutations",
        "gridded_cayley_permutations",
        "vertical_insertion_encoding",
        "horizontal_ins_enc",
        "tilescope",
        "vatters_method",
    ],
    install_requires=[
        "typing",
        "comb_spec_searcher",
    ],  # external packages as dependencies
)
