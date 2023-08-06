"""
RSA 4/2/23


"""

import os
from os.path import exists
import urllib.request
import threading
from Bio.PDB.MMCIFParser import MMCIFParser        
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
from Bio.PDB.PDBParser import PDBParser

import warnings
from Bio import BiopythonWarning
warnings.simplefilter('ignore', BiopythonWarning)

class PdbObject(object):
    def __init__(self, pdb_code, location="", delete=True, cif=False, emmap=False):
        # PUBLIC INTERFACE
        self.pdb_code = pdb_code        
        self.ebi_link = f"https://www.ebi.ac.uk/pdbe/entry/pdb/{pdb_code}"
        self.cif_link = f"https://www.ebi.ac.uk/pdbe/entry-files/download/{pdb_code}.cif"
        self.pdb_link = f"https://www.ebi.ac.uk/pdbe/entry-files/download/pdb{pdb_code}.ent"
        self.ccp4_link = f"https://www.ebi.ac.uk/pdbe/entry-files/{self.pdb_code}.ccp4"
        self.diff_link = f"https://www.ebi.ac.uk/pdbe/entry-files/{self.pdb_code}_diff.ccp4"
        self.resolution = ""
        self.exp_method = ""
        self.map_header = {}
        self.valid = False
        # Private data
        self._ccp4_binary = None
        self._diff_binary = None        
        # PRIVATE INTERFACE
        self._location = location
        self._delete = delete
        self._cif=cif
        self._emmap=emmap
        self._download_tag = f"{location}{pdb_code}.tag"
        self._download_end = f"{location}{pdb_code}.end"
        self._filepath_cif = f"{location}{pdb_code}.cif"
        self._filepath_pdb = f"{location}{pdb_code}.pdb"
        self._filepath_ccp4 = f"{location}{pdb_code}.ccp4"
        self._filepath_diff = f"{location}{pdb_code}_diff.ccp4"
                

    def getHeaders(self):
        mhs = []
        for mh in self.map_header.items():
            mhs.append(mh)
        return mhs

    def fetch_data_thread(self):
        if exists(self._download_tag):
            print("Downloading...")
            return False
        elif exists(self._download_end):            
            return True
        else:
            with open(self._download_tag,"w") as fw:
                fw.writelines(["downloading"])
            download_thread = threading.Thread(target=self.fetch_data, args=())
            download_thread.start()
            return False

    def fetch_data(self):
        if self._cif:
            self._fetch_pdbdata_cif()
        else:
            self._fetch_pdbdata_pdb()

        self.load_pdbdata()
        
        if self._emmap:
            if 'x-ray' in self.exp_method:
                self._fetch_maplink_xray()                
            else:
                self._fetch_maplink_em()                
        
        with open(self._download_end,"w") as fw:
                fw.writelines(["downloaded"])

        if exists(self._download_tag):
            os.remove(self._download_tag)

    def load_pdbdata(self):
        if self._cif:
            structure = MMCIFParser().get_structure(self.pdb_code, self._filepath_cif)
            self._struc_dict = MMCIF2Dict(self._filepath_cif)
            self.resolution = structure.header["resolution"]
            self.exp_method = structure.header["structure_method"]            
        else:
            structure = PDBParser(PERMISSIVE=True).get_structure(self.pdb_code, self._filepath_pdb)
            self._struc_dict = MMCIF2Dict(self._filepath_pdb)
            self.resolution = structure.header["resolution"]
            self.exp_method = structure.header["structure_method"]            

    def load_data(self):
        
        self.valid = True
        try:
            self.load_pdbdata()

            if self._emmap:
                if 'x-ray' in self.exp_method:         
                    with open(self._filepath_ccp4, mode='rb') as file:
                        self._ccp4_binary = file.read()
                    with open(self._filepath_diff, mode='rb') as file:
                        self._diff_binary = file.read()
                    self._create_mapheader()
                else:                
                    self._create_mapdata_em()
        except:
            self.valid = False


    def clear_data(self):
        self._clear_pbbdata()
        self._clear_mapdata()
        if self._delete and exists(self._download_end):
                os.remove(self._download_end)
        if self._delete and exists(self._download_tag):
                os.remove(self._download_tag)
    

    #################################################
    ############ PRIVATE INTERFACE ##################
    #################################################    
    def _fetch_pdbdata_cif(self):        
        try:            
            if not exists(self._filepath_cif):            
                urllib.request.urlretrieve(self.cif_link, self._filepath_cif)                                
        except:            
            return False
        return True
        
    def _fetch_pdbdata_pdb(self):        
        try:            
            if not exists(self._filepath_pdb):
                urllib.request.urlretrieve(self.pdb_link, self._filepath_pdb)                
            
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


    def _clear_pbbdata(self):
        if self._delete and exists(self._filepath_cif):
                os.remove(self._filepath_cif)
        if self._delete and exists(self._filepath_pdb):
                os.remove(self._filepath_pdb)
        
    
    def _clear_mapdata(self):        
        if self._delete and exists(self._filepath_ccp4):
                os.remove(self._filepath_ccp4)
        if self._delete and exists(self._filepath_diff):
                os.remove(self._filepath_diff)
