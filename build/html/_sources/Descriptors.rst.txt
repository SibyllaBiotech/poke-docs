===========
Descriptors
===========

Poké produce a csv file with all the pockets found. The file contains the following columns:

``OutputFrame`` The index of the frame in the output trajectory. When no extraction or sorting is performed it is equal to the input frame. See the section on the output trajectory for more details.

``OriginalFrame`` The index of the frame in the input trajectory. When multiple trajectories are concatenated it is the index in the concatenated trajectory. Notice that the reference frame is not included in the count.

``PocketResid`` If there are multiple pockets in the same frame, the volume points are written with the resid specified in this column. Useless if sorting is performed.

``Score`` The score assigned to the pocket by the neural network model. It is a measure of the pocket druggability.

``Volume`` The low-energy space available to the ligand measured in Å³. It is proportional to the number of points of the pocket and the grid spacing.

``Surface`` Proportional to the number of superficial points of the pockets measured in Å². A point is defined when the number of adjacent points is less than 5. The surface-to-volume ratio can provide insight into the shape of the pocket.

``Lengths`` Three numbers representing the average lengths of the pocket measured along orthogonal axis. They are computed as the squared root of the eigenvalues of the covariance matrix of the points.

``Hydrophobicity`` Fraction of atoms belonging to the pocket with a absolute partial charge less than 0.3e.

``Enclosure`` An indicator of the enclosure of the pocket computed comparing the number of atoms neighboring the pocket and its surface.

``#PolarAtoms`` Number of atoms belonging to the pocket with a absolute partial charge between 0.3e and 0.7e.

``#ChargedAtoms`` Number of atoms belonging to the pocket with a absolute partial charge greater than 0.7e.
