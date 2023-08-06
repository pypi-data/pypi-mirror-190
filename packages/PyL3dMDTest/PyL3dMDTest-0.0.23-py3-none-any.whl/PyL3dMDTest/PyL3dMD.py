# -*- coding: utf-8 -*-
"""
Created on Thu December 10 11:41:02 2022

@author: Pawan Panwar, Quanpeng Yang, Ashlie Martini


PyL3dMD: Python LAMMPS 3D Molecular Dynamics/Descriptors
Copyright (C) 2022  Pawan Panwar, Quanpeng Yang, Ashlie Martini

This file is part of PyL3dMD.

PyL3dMD is free software: you can redistribute it and/or modify 
it under the terms of the GNU General Public License as published 
by the Free Software Foundation, either version 3 of the License, 
or (at your option) any later version.

PyL3dMD is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
 along with PyL3dMD. If not, see <https://www.gnu.org/licenses/>.
"""


import time
import numpy as np
import pandas as pd
import multiprocessing as mp

from . import getinfofromlammpsdatafile
from . import getinfofromlammpstrajfile
from . import getatomicproperties
from . import getadjacencyanddistancematrices
from . import rdf
from . import morse
from . import moreaubroto
from . import geary
from . import moran
from . import whim
from . import getaway
from . import cpsa
from . import geometricdescriptors
from . import topologyconnectivity3Ddescriptors

class PyL3dMD:
    def __init__(self, datafilename, dumpfilename, FromFrame=None, ToFrame=None, FrameInterval=None, numberofcores=None):
        self.datafilename = datafilename
        self.dumpfilename = dumpfilename
        if numberofcores is None:
            self.numberofcores = mp.cpu_count()
        else:
            self.numberofcores = numberofcores

        ############################################ PRE-PROCESSING ###########################################

        # GET ALL INFORMATIONS FROM LAMMPS DATA FILE
        idAtoms, idMols, atomTypes, atomCharges, atomMasses, atomSection, bondSection = getinfofromlammpsdatafile.getalldatafileinfo(datafilename)
        self.eachMolsNumIdx, self.eachMolsIdx, self.eachMolsMass, self.eachMolsCharge, self.eachMolsBonds, self.eachMolsAngles, self.eachMolsDihedrals = getinfofromlammpsdatafile.arragebymolecule(
            idAtoms, idMols, atomMasses, atomCharges, bondSection)
        numAtoms = len(idAtoms)  # num of atoms in the simulation box
        self.numMols = max(idMols)  # num of molecules in the simulation box

        # GET ALL INFORMATIONS FROM LAMMPS DUMP/TRAJECTORY FILE
        dataXdim, dataYdim, dataZdim, boxlengths = getinfofromlammpstrajfile.getboxboundariesANDlengths(dumpfilename)
        colid, colmol, coltype, colx, coly, colz, needToUnwrap = getinfofromlammpstrajfile.getcolumns(dumpfilename)
        datadump, self.datadumpdict, self.nframes = getinfofromlammpstrajfile.readlammpsdumpfile(dumpfilename, numAtoms, colid, colmol, coltype,
                                                                       colx, coly,
                                                                       colz, needToUnwrap, boxlengths)
                                                                       
        # define from/to frames and interval of the trajactory file for the descriptor calculation
        if FromFrame is None:
            self.FromFrame = 0
        else:
            self.FromFrame = FromFrame
        if ToFrame is None:
            self.ToFrame = self.nframes
        else:
            self.ToFrame = ToFrame
        if FrameInterval is None:
            self.FrameInterval = 1
        else:
            self.FrameInterval = FrameInterval

        # DENSITY OF THE SIMULATION BOX AT EACH TIME FRAMES
        self.rho = []
        massBox = np.sum(atomMasses)  # Sum of mass of all atoms in the simulation box
        for i in range(self.nframes):
            # Length of the simulation box at a time frame
            lx = boxlengths[i, 0]
            ly = boxlengths[i, 1]
            lz = boxlengths[i, 2]

            # Volume of the simulation box at a time frame
            volBox = lx * ly * lz  # [ÅxÅxÅ]

            # Density at a time frame
            self.rho.append(self.caldensity(massBox, volBox))  # [g/cc]

        # GET ALL ATOMIC PROPERTIES
        _, _, _, _, self.eachMolsRc, self.eachMolsm, self.eachMolsV, self.eachMolsEn, self.eachMolsalapha, self.eachMolsIP, self.eachMolsEA = getatomicproperties.getatomicproperties(
            atomMasses, self.eachMolsIdx)

        # Get adjacency and distnace matrices
        self.eachMolsAdjMat, self.eachMolsDisMat = getadjacencyanddistancematrices.getadjANDdismatrices(self.eachMolsMass, self.eachMolsBonds)

    def start(self):
        print(f"Started pool with {self.numberofcores} workers.")
        t1 = time.perf_counter()
        items = []
        for i in range(self.numMols):
            for j in range(self.FromFrame,self.ToFrame,self.FrameInterval):
                items.append((i, j))

                # create the process pool
        with mp.Pool(processes=self.numberofcores) as pool:

            ans = []
            # call the same function with different data in parallel
            for result in pool.starmap(self.caldescriptors, items):
                # report the value to show progress
                ans.append(result)
         
        # Convert to dataframe
        df = pd.DataFrame.from_dict(ans)

        # split dataframe using gropuby
        splits = list(df.groupby("molecule"))
        for i in range(self.numMols):
            # Dump descriptors of a molecule for all time frames
            splits[0][1].to_csv('Molecule_' + str(i + 1) + '.csv')

        t2 = time.perf_counter()
        print(f'Finished in {t2 - t1} seconds')

    def caldensity(self, massBox, volBox):
        """
        simulation calculated density of the fluid [g/cc]
        """
        NA = 6.0221408e+23  # Avogadro's number [1/mol]
        volBoxcc = volBox * 1.0E-24  # volume of the simulation box [cc]

        # Simulation-calculated density [g/cc]
        rho = (massBox / volBoxcc) * (1.0 / NA)
        return rho

    def calgeometricdistancematrix(self, xyz):
        """
        Calculate Euclidean Distance of atoms in a molecule - (numAtoms x numAtoms)
        """
        onesMat = np.ones([len(xyz), len(xyz)])
        Gx = onesMat * xyz[:, 0] - np.transpose(onesMat * xyz[:, 0])
        Gy = onesMat * xyz[:, 1] - np.transpose(onesMat * xyz[:, 1])
        Gz = onesMat * xyz[:, 2] - np.transpose(onesMat * xyz[:, 2])

        # Geometric Distance Matrix
        G = np.sqrt(Gx ** 2 + Gy ** 2 + Gz ** 2)
        return G

    ######################################## CALCULATE DESCRIPTORS OF ALL MOLECULES AT ALL TIME FRAMES ########################################
    def caldescriptors(self, i, j):
        mass = self.eachMolsMass[i]
        charge = self.eachMolsCharge[i]
        bond = self.eachMolsBonds[i]
        angle = self.eachMolsAngles[i]
        dihedral = self.eachMolsDihedrals[i]
        disMat = self.eachMolsDisMat[i]
        adjMat = self.eachMolsAdjMat[i]
        xyz = self.datadumpdict[j][i][:, 3:6]
        density = self.rho[j]

        # Atomic properties
        apRc = self.eachMolsRc[i]
        apm = self.eachMolsm[i]
        apV = self.eachMolsV[i]
        apEn = self.eachMolsEn[i]
        apalapha = self.eachMolsalapha[i]
        apIP = self.eachMolsIP[i]
        apEA = self.eachMolsEA[i]

        # calculate Geometric matrix
        G = self.calgeometricdistancematrix(xyz)

        # Calculate all descriptors
        RDF = rdf.getrdfdescriptors(G, charge, apm, apV, apEn, apalapha, apIP, apEA)  # 30*8 = 240
        MoRSE = morse.getmorsedescriptors(G, charge, apm, apV, apEn, apalapha, apIP, apEA)  # 30*8 = 240
        ATS = moreaubroto.getmoreaubrotodescriptors(G, charge, apm, apV, apEn, apalapha, apIP, apEA)  # 30*7 = 210
        GATS = geary.getgearyindices(G, charge, apm, apV, apEn, apalapha, apIP, apEA)  # 30*7 = 210
        MATS = moran.getmorandescriptors(G, charge, apm, apV, apEn, apalapha, apIP, apEA)  # 30*7 = 210
        WHIM = whim.getwhimdescriptors(xyz, charge, apm, apV, apEn, apalapha, apIP, apEA)  # 14*8 = 112
        GETAWAY = getaway.getgetawayhatsindexes(xyz, mass, bond, charge, apm, apV, apEn, apalapha, apIP, apEA)  # 14*8 = 112
        CPSA = cpsa.getcpsadescriptors(xyz, charge, apRc)  # 30

        GMdes, DDMdes = geometricdescriptors.calgeometricdescriptors(xyz, mass, charge, bond, angle, dihedral, density,
                                                disMat)  # GMdes = 85, DDMdes = 10
        TCdes = topologyconnectivity3Ddescriptors.caltopologyconnectivitydescriptors(xyz, mass, bond, angle, dihedral, adjMat, disMat)  # TCdes = 27

        others = {'molecule': i + 1, 'Timeframe': j, 'rho': density}

        # Combine all dictionaries into a single dictionary to return/store
        res = {**others, **GMdes, **DDMdes, **TCdes, **RDF, **MoRSE, **ATS, **GATS, **MATS, **WHIM, **GETAWAY, **CPSA}
        return res
