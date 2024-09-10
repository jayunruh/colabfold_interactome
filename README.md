# colabfold_interactome
## Workflow/tutorial for colabfold interactome virtual screening.

This is a tutorial with workflow scripts for performing colabfold interactome virtual screening. Before starting please install colabfold as described in https://github.com/YoshitakaMo/localcolabfold as well as mmseqs2 as described in https://github.com/soedinglab/MMseqs2 and in https://github.com/sokrypton/ColabFold.

The tutorial is in [CF_Interactome_Screening_Tutorial.html](CF_Interactome_Screening_Tutorial.html).

The tutorial often loads modules that may be named differently on your HPC environment.  Several scripts rely on my jpdbtools2.py module available here: https://github.com/jayunruh/Jay_pdbtools.  In some python scripts the path to that file needs to be changed.

## Dependencies

In addition to the dependencies mentioned above, this code depends on fairly standard python tools including glob, pandas, argparse, matplotlib, numpy, json, and scipy.
