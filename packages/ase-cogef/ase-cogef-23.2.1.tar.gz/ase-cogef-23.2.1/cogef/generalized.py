from pathlib import Path
import numpy as np

from ase import io
from ase.constraints import FixBondLength, FixBondLengths
from ase.parallel import parprint, world
from ase.utils import deprecated, IOContext

from cogef import COGEF
from cogef.utilities import mkparent


class COGEF1D(COGEF, IOContext):
    def __init__(self, atom1, atom2, initialize=None,
                 txt='-', comm=world, **kwargs):
        self.initialize = initialize
        self.txt = self.openfile(txt, comm)
        COGEF.__init__(self, atom1, atom2, **kwargs)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value is None:
            self._name = str(self.__class__.__name__).lower()
        else:
            self._name = str(value)

        # add pull positions as extension if not already there
        ext = '_{0}_{1}'.format(self.atom1, self.atom2)
        if ext not in self._name:
            self._name += ext

        # name change => remove images
        self._images = []
        self.look_for_images()

    def shift_and_optimize(self, mother, dstep, index):
        """Shift atoms by dstep and optimze

        mother: Atoms
          the Atoms object to be shifted
        dstep: float
          value of the shift
        index:
          index of atoms needed for optimizer trajectory filename

        retruns relaxed atoms
        """
        atoms = mother.copy()

        # file name for optimizer trajectory
        optimizer_traj = (Path(self.name)
                          / 'image{0}.traj'.format(index))

        # check for already existing optimization history
        try:
            atoms = io.read(optimizer_traj)
        except FileNotFoundError:
            mkparent(optimizer_traj)
            atoms = mother.copy()
            self.shift_atoms(atoms, dstep)

        # make sure my constraint is there before initialize
        self.add_my_constraint(atoms)

        if self.initialize is None:
            atoms.calc = self.images[-1].calc
        else:
            # let the user provided function take care about the image
            atoms = self.initialize(atoms)

        # make sure, my constraint is not accidently removed
        self.add_my_constraint(atoms)

        return self._optimize(atoms)

    def _optimize(self, atoms):
        opt = self.optimizer(atoms, logfile=self.txt)
        opt.run(fmax=self.fmax)
        return atoms

    def move(self, dstep, steps):
        if len(self.images) == 1:
            # make sure first image is relaxed
            self.images[0] = self._optimize(self.images[0])

        filename = Path(self.trajname)
        if filename.is_file():
            trajectory = io.Trajectory(filename, 'a')
            assert len(trajectory) == len(self.images)
        else:
            mkparent(filename)
            trajectory = io.Trajectory(filename, 'w')
            for image in self.images:
                trajectory.write(image)

        for i in range(steps):
            parprint(self.__class__.__name__, f'step {i + 1}/{steps}',
                     file=self.txt)
            self.images.append(
                self.shift_and_optimize(
                    self.images[-1], dstep=dstep, index=len(self.images)))
            trajectory.write(self.images[-1])

    @deprecated(DeprecationWarning('Please use move'))
    def pull(self, dstep, steps, initialize=None):
        self.move(dstep, steps)

    def __len__(self):
        return len(self.images)

    def shift_atoms(self, atoms, stepsize):
        """Shift atoms by stepsize"""
        a1 = atoms[self.atom1]
        a2 = atoms[self.atom2]
        nvec12 = a2.position - a1.position
        nvec12 /= np.linalg.norm(nvec12)
        # shift mass weighted
        a1.position -= stepsize * a2.mass / (a1.mass + a2.mass) * nvec12
        a2.position += stepsize * a1.mass / (a1.mass + a2.mass) * nvec12

    def add_my_constraint(self, atoms):
        """make sure my constraint is present"""
        self.remove_my_constraint(atoms)
        atoms.constraints.append(self.get_constraint())

    def remove_my_constraint(self, atoms):
        """make sure my constraint is not present"""
        mydict = self.get_constraint().todict()
        constraints = []
        for i, constraint in enumerate(atoms.constraints):
            if constraint.todict() != mydict:
                constraints.append(constraint)
        atoms.constraints = constraints

    def get_constraint(self):
        # we need to create a new constraint for every image
        return FixBondLength(self.atom1, self.atom2)

    def get_distances(self):
        return np.array([img.get_distance(self.atom1, self.atom2)
                         for img in self.images])

    def get_energies(self):
        return np.array([img.get_potential_energy()
                         for img in self.images])

    def get_forces(self):
        """Return forces due to constraint"""
        # XXX implement yourself?
        forces, distances = self.get_force_curve('use_forces')
        return forces

    def forces_from_energies(self):
        """Forces from energy derivatives

        returns: distances and corresponding forces
        """
        # XXX implement yourself?
        forces, distances = self.get_force_curve('use_energies')
        return distances, forces

    def look_for_images(self):
        """Check whether there are images already based on the name"""
        try:
            self.images = io.Trajectory(self.trajname)
            parprint(self.__class__.__name__ + ': read', len(self.images),
                     'images from', self.trajname, file=self.txt)
        except FileNotFoundError:
            pass


class Concerted(COGEF1D):
    """COGEF1D for concerted variation of two bonds"""
    def __init__(self, pairs, *args, **kwargs):
        """
        pair1: indices of first bond
        pair2: indices of second bond
        """
        self.pairs = pairs
        COGEF1D.__init__(self, *pairs[0], *args, **kwargs)

    def shift_atoms(self, atoms, stepsize):
        """Shift atoms by stepsize"""
        for i1, i2 in self.pairs:
            a1 = atoms[i1]
            a2 = atoms[i2]
            nvec12 = a2.position - a1.position
            nvec12 /= np.linalg.norm(nvec12)
            # shift mass weighted
            a1.position -= stepsize * a2.mass / (a1.mass + a2.mass) * nvec12
            a2.position += stepsize * a1.mass / (a1.mass + a2.mass) * nvec12

    def get_constraint(self):
        # we need to create a new constraint for every image
        return FixBondLengths(self.pairs)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value is None:
            self._name = str(self.__class__.__name__).lower()
        else:
            self._name = str(value)

        # add pull positions as extension if not already there
        for pair in self.pairs:
            ext = '_{0}_{1}'.format(*pair)
            if ext not in self._name:
                self._name += ext

        # name change => remove images
        self._images = []
        self.look_for_images()
