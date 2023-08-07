"""
RSA 4/2/23


"""

import os
from os.path import exists
import urllib.request
from Bio.PDB.MMCIFParser import MMCIFParser        
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
from Bio.PDB.PDBParser import PDBParser

import warnings
from Bio import BiopythonWarning
warnings.simplefilter('ignore', BiopythonWarning)

class PdbObject(object):
    def __init__(self, pdb_code, directory="", delete=False, cif=False):
        # PUBLIC INTERFACE
        self.pdb_code = pdb_code        
        self.ebi_link = f"https://www.ebi.ac.uk/pdbe/entry/pdb/{pdb_code}"                
        self.resolution = ""
        self.exp_method = ""
        self.map_header = {}
        # Private data
        self._ccp4_binary = None
        self._diff_binary = None        
        self.loaded = False        
        # PRIVATE INTERFACE
        self._directory = directory
        self._delete = delete
        self._cif=cif
        if cif:
            self._filepath = f"{directory}{pdb_code}.cif"
            self.pdb_link = f"https://www.ebi.ac.uk/pdbe/entry-files/download/{pdb_code}.cif"
        else:        
            self._filepath = f"{directory}{pdb_code}.pdb"
            self.pdb_link = f"https://www.ebi.ac.uk/pdbe/entry-files/download/pdb{pdb_code}.ent"
        
        self._filepath_ccp4 = f"{self._directory}{self.pdb_code}.ccp4"
        self._filepath_diff = f"{self._directory}{self.pdb_code}_diff.ccp4"
        self.ccp4_link = f"https://www.ebi.ac.uk/pdbe/entry-files/{self.pdb_code}.ccp4"
        self.diff_link = f"https://www.ebi.ac.uk/pdbe/entry-files/{self.pdb_code}_diff.ccp4"
                                
    def exists(self):
        if self.exists_pdb():
            if self.exists_map():
                return True
        
        return False
    
    def exists_pdb(self):
        if exists(self._filepath):
            return True
        else:
            return False
    
    def exists_map(self):
        self.load_pdb()
        if 'x-ray' in self.exp_method:
            if exists(self._filepath_ccp4) and exists(self._filepath_diff):                
                self.loaded = True
                return True        
            else:
                return False
        else:
            self.loaded = True
            return True # it doesn;t NOT exists anyway
    
    def download(self):
        if not self.exists_pdb():
            self.download_pdb()
        if not self.exists_map():
            self.download_map()
    
    def download_pdb(self):
        self._fetch_pdbdata()

    def download_map(self):
        if not self.loaded:
            self.load_pdb()            
        if 'x-ray' in self.exp_method:
            self._fetch_maplink_xray()
        self.loaded = True
    
    def load(self):
        self.load_pdb()
        if 'x-ray' in self.exp_method:            
            self.load_map()

    def load_pdb(self):
        if self._cif:
            structure = MMCIFParser().get_structure(self.pdb_code, self._filepath)
        else:
            structure = PDBParser(PERMISSIVE=True).get_structure(self.pdb_code, self._filepath)
        self._struc_dict = MMCIF2Dict(self._filepath)
        self.resolution = structure.header["resolution"]
        self.exp_method = structure.header["structure_method"]            

    def load_map(self):
        try:
            with open(self._filepath_ccp4, mode='rb') as file:
                self._ccp4_binary = file.read()        
            with open(self._filepath_diff, mode='rb') as file:
                self._diff_binary = file.read()
            self._create_mapheader()
            self.loaded = True
        except:        
            self.loaded = False

    #################################################
    ############ PRIVATE INTERFACE ##################
    #################################################
    def _fetch_pdbdata(self):
        try:
            print(self.pdb_link, self._filepath)            
            urllib.request.urlretrieve(self.pdb_link, self._filepath)                                
        except:            
            return False
        return True
        
    def _fetch_maplink_xray(self):                
        if not exists(self._filepath_ccp4):            
            urllib.request.urlretrieve(self.ccp4_link, self._filepath_ccp4)
        if not exists(self._filepath_diff):            
            urllib.request.urlretrieve(self.diff_link, self._filepath_diff)

                        
    def _fetch_maplink_em(self):        
        em_link = ""

    def _create_mapheader(self):
        i=0
        self.map_header["01_NC"] = int.from_bytes(self._ccp4_binary[i:i+4], byteorder='little', signed=False)
        i+=4
        self.map_header["02_NR"] = int.from_bytes(self._ccp4_binary[i:i+4], byteorder='little', signed=False)
        i+=4
        self.map_header["03_NS"] = int.from_bytes(self._ccp4_binary[i:i+4], byteorder='little', signed=False)
        i+=4
        self.map_header["04_MODE"] = int.from_bytes(self._ccp4_binary[i:i+4], byteorder='little', signed=False)
        
        
        
    def _create_mapdata_em(self):
        ccp4_link = ""
        em_link = ""


    def cleanup(self):
        pass
