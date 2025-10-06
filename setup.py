from setuptools import setup, find_namespace_packages

setup(
    name="cperms_ins_enc",
    version="1.0.0",
    description="A module for enumerating Cayley permutations using the insertion encoding.",
    author="Christian Bean, Abigail Ollson",
    author_email="a.n.ollson@keele.ac.uk",
    packages=find_namespace_packages(),
    keywords="enumerative combinatorics pattern avoidance cayley permutations insertion encoding",
    install_requires=[
        "comb_spec_searcher",
        "cayley_perms @ git+https://github.com/Ollson2921/CayleyPerms",
    ],
)
