from pathlib import Path

from postopus import Run

"""
This script is for testing. It provides a collection of calls
endusers would do.
"""

if __name__ == "__main__":
    # This works
    repodir = Path(__file__).parents[3]
    exampleinp = repodir / "tests" / "data" / "archimedean_spiral"
    print(exampleinp)
    run = Run(exampleinp)
    print("Data Container: ", end="")
    print(run)
    print("Modes Container: ", end="")
    print(run.Maxwell.system_data)
    print("Maxwell Fields: ", end="")
    print(run.Maxwell.td.fields.keys())
    print("e_field.z Field: ", end="")
    print(run.Maxwell.td.e_field.z)
    print("Number of iterations for 'e_field.z' field: ", end="")
    print(run.Maxwell.td.e_field.z.n_iterations)
    print("IDs for iterations: ", end="")
    print(run.Maxwell.td.e_field.z.iteration_ids)
    print("Data from single iteration: ", end="")
    print(run.Maxwell.td.e_field.z.get(0, source="z=0").values)

    # For reference, data still can be accessed with the usual dict syntax:
    # run.Maxwell.td.e_field.z.iteration(0, outputformat="z=0").data replaces
    # run.systems["Maxwell"].modes["td"].fields["e_field"].dimensions["z"}
    # .iteration(5, outputformat="z=0").data

    data = run.Maxwell.td.e_field.z.get(0, source="z=0").values
    xarr = run.Maxwell.td.e_field.z.get(0, source="z=0")
    print(xarr)
