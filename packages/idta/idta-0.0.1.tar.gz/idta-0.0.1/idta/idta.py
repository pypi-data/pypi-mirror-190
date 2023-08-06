import pandas as pd
import json
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import subprocess
import os
import urllib.request
import numpy as np
from Bio.PDB import *
import math
from IPython.display import display
import nglview


class Drug_module:

    def __init__(self, json_file):
        self.json_file = json_file
        self.results_list = []
        self.results_list_in_pocket = []

    def read_json_get_hcs(self):
        with open(self.json_file) as hcs_json_data:
            hcs_json = json.load(hcs_json_data)

        hcs_seq = []
        for i in range(len(hcs_json)):
            hcs_seq.append(hcs_json[i]["sequence"])
        return hcs_seq

    def write_fasta_from_seq_list(self):
        hcs_seq = self.read_json_get_hcs()
        records = []
        for i in range(len(hcs_seq)):
            records.append(SeqRecord(Seq(hcs_seq[i]), description=hcs_seq[i]))
        SeqIO.write(records, "hcs_seq.fasta", "fasta")

    def do_pdb_blast(self):
        # Blastp should be accessible and tax id should given from a string.(input, output and taxid should be dynamic)
        command_line_blastp = ["blastp", "-query", "hcs_seq.fasta", "-matrix", "PAM30", "-db", "./pdbaa",
                               "-taxids", "11320", "-outfmt", "10", "-out", "hcs_pdb_blast_11320.csv"]

        subprocess.call(command_line_blastp)

    def filtering_blast_output(self):
        blast_output_df = pd.read_csv("hcs_pdb_blast_11320.csv",
                                      names=["query", "subject", "perc_identity",
                                             "length", "mismatch", "gapopen", "qstart",
                                             "qend", "sstart", "send", "evalue", "bitscore"])

        blast_output_df["q_len"] = blast_output_df["query"].apply(lambda x: len(x))
        blast_output_df_filtered = blast_output_df.loc[
            (blast_output_df['evalue'] <= 0.05) & (blast_output_df['length'] == blast_output_df['q_len']) & (
                        blast_output_df['perc_identity'] == 100)].reset_index(drop=True)
        blast_output_df_filtered["pdb"] = blast_output_df_filtered["subject"].apply(lambda x: x[:4])
        blast_output_df_filtered["chain"] = blast_output_df_filtered["subject"].apply(lambda x: x[5:])
        return blast_output_df_filtered

    def get_pdb_files(self):

        blast_output_df_filtered = self.filtering_blast_output()

        blast_output_df_filtered["resolution"] = np.nan
        blast_output_df_filtered["method"] = np.nan

        for i in range(len(blast_output_df_filtered["pdb"])):
            pdburl = blast_output_df_filtered["pdb"][i] + ".pdb"
            os.chdir("./PDB")
            urllib.request.urlretrieve(url="http://files.rcsb.org/download/" + pdburl, filename=pdburl)
            parser = PDBParser()
            structure = parser.get_structure(blast_output_df_filtered["pdb"][i], pdburl)
            blast_output_df_filtered["resolution"][i] = structure.header["resolution"]
            blast_output_df_filtered["method"][i] = structure.header["structure_method"]
            os.chdir("../../")

        for i in range(len(set(blast_output_df_filtered["query"]))):
            globals()[f"seq{i}_df"] = blast_output_df_filtered[
                blast_output_df_filtered["query"] == list(set(blast_output_df_filtered["query"]))[i]]

        for i in range(len(set(blast_output_df_filtered["query"]))):
            if globals()[f"seq{i}_df"][globals()[f"seq{i}_df"]["method"] == "x-ray diffraction"].empty == False:
                self.results_list.append(
                    globals()[f"seq{i}_df"].loc[globals()[f"seq{i}_df"]['method'] == "x-ray diffraction"].loc[
                        globals()[f"seq{i}_df"].loc[globals()[f"seq{i}_df"]['method'] == "x-ray diffraction"][
                            'resolution'] ==
                        globals()[f"seq{i}_df"].loc[globals()[f"seq{i}_df"]['method'] == "x-ray diffraction"][
                            'resolution'].min()].reset_index().values.tolist())
            elif globals()[f"seq{i}_df"][globals()[f"seq{i}_df"]["method"] == "solution nmr"].empty == False:
                self.results_list.append(
                    globals()[f"seq{i}_df"].loc[globals()[f"seq{i}_df"]['method'] == "solution nmr"].loc[
                        globals()[f"seq{i}_df"].loc[globals()[f"seq{i}_df"]['method'] == "solution nmr"][
                            'resolution'] ==
                        globals()[f"seq{i}_df"].loc[globals()[f"seq{i}_df"]['method'] == "solution nmr"][
                            'resolution'].min()].reset_index().values.tolist())
            elif globals()[f"seq{i}_df"][globals()[f"seq{i}_df"]["method"] == "solid-state nmr"].empty == False:
                self.results_list.append(
                    globals()[f"seq{i}_df"].loc[globals()[f"seq{i}_df"]['method'] == "solid-state nmr"].loc[
                        globals()[f"seq{i}_df"].loc[globals()[f"seq{i}_df"]['method'] == "solid-state nmr"][
                            'resolution'] ==
                        globals()[f"seq{i}_df"].loc[globals()[f"seq{i}_df"]['method'] == "solid-state nmr"][
                            'resolution'].min()].reset_index().values.tolist())
            elif globals()[f"seq{i}_df"][globals()[f"seq{i}_df"]["method"] == "electron microscopy"].empty == False:
                self.results_list.append(
                    globals()[f"seq{i}_df"].loc[globals()[f"seq{i}_df"]['method'] == "electron microscopy"].loc[
                        globals()[f"seq{i}_df"].loc[globals()[f"seq{i}_df"]['method'] == "electron microscopy"][
                            'resolution'] ==
                        globals()[f"seq{i}_df"].loc[globals()[f"seq{i}_df"]['method'] == "electron microscopy"][
                            'resolution'].min()].reset_index().values.tolist())

        return self.results_list

    def pocket_control(self):

        pdb_ids_for_hcs = []
        for i in range(len(self.results_list)):
            pdb_ids_for_hcs.append(self.results_list[i][0][2])

        uniq_pdb_ids_for_hcs = list(set(pdb_ids_for_hcs))

        os.chdir("./PDB")
        os.mkdir("./pocket_prediction_results")

        for i in range(len(uniq_pdb_ids_for_hcs)):
            !./p2rank_2.4 prank predict - f {uniq_pdb_ids_for_hcs[i].split("_")[0]}".pdb" - o. / pocket_prediction_results

        for i in range(len(uniq_pdb_ids_for_hcs)):
            globals()[f"df_{uniq_pdb_ids_for_hcs[i]}"] = pd.read_csv(
                "./pocket_prediction_results/" + uniq_pdb_ids_for_hcs[i].split("_")[0] + ".pdb_residues.csv")

        os.chdir("../../")

        for i in range(len(uniq_pdb_ids_for_hcs)):
            globals()[f"df_{uniq_pdb_ids_for_hcs[i]}_filtered"] = globals()[f"df_{uniq_pdb_ids_for_hcs[i]}"].loc[
                (globals()[f"df_{uniq_pdb_ids_for_hcs[i]}"]['chain'] == uniq_pdb_ids_for_hcs[i].split("_")[1]) & (
                            globals()[f"df_{uniq_pdb_ids_for_hcs[i]}"][' pocket'] > 0)]

        for i in range(len(uniq_pdb_ids_for_hcs)):
            globals()[f"df_{uniq_pdb_ids_for_hcs[i]}_filtered"] = globals()[
                f"df_{uniq_pdb_ids_for_hcs[i]}_filtered"].reset_index()
            del globals()[f"df_{uniq_pdb_ids_for_hcs[i]}_filtered"]["index"]

        hcs_on_pocket = []

        for i in range(len(self.results_list)):
            hcs_pos_range = list(range(self.results_list[i][0][9], self.results_list[i][0][10]))
            for j in range(len(globals()[f"df_{self.results_list[i][0][2]}_filtered"])):
                if globals()[f"df_{self.results_list[i][0][2]}_filtered"][" residue_label"][j] in hcs_pos_range:
                    print(self.results_list[i][0][1], ":",
                          globals()[f"df_{self.results_list[i][0][2]}_filtered"][" residue_name"][j],
                          "on HCS position",
                          globals()[f"df_{self.results_list[i][0][2]}_filtered"][" residue_label"][j],
                          "found in pocket", globals()[f"df_{self.results_list[i][0][2]}_filtered"][" pocket"][j])
                    hcs_on_pocket.append(self.results_list[i][0][1])
            else:
                print(self.results_list[i][0][1], ":", "HCS not found on binding pocket")

        if len(hcs_on_pocket) == 0:
            print("None of the HCS found on the pocket.")
        else:
            for i in range(len(list(set(hcs_on_pocket)))):
                self.results_list_in_pocket.append(
                    [x for x in self.results_list if x[0][1] == list(set(hcs_on_pocket))[i]])

        return self.results_list_in_pocket

    def calculate_center_of_box(self):

        for i in range(len(self.results_list_in_pocket)):

            # Parsing hcs cordinates
            parser = PDBParser()
            os.chdir("./PDB")
            structure = parser.get_structure(self.results_list_in_pocket[i][0][0][14],
                                             self.results_list_in_pocket[i][0][0][14] + ".pdb")
            os.chdir("../../")
            coord = []

            for chains in structure:
                for chain in chains:
                    if chain.id == self.results_list_in_pocket[i][0][0][15]:
                        for index, residue in enumerate(chain):
                            coord.append([])
                            for j in residue:  # we get the coordinates
                                coord[index].append(j.get_coord())

            aa_residues = []

            for chains in structure:
                for chain in chains:
                    if chain.id == self.results_list_in_pocket[i][0][0][15]:
                        for residue in chain.get_list():
                            residue_id = residue.get_id()
                            hetfield = residue_id[0]
                            if hetfield[0] == " ":
                                aa_residues.append(residue.get_resname())

            all_aa = []

            for k in aa_residues:
                all_aa.append(Polypeptide.three_to_one(k))

            all_aa = ''.join(all_aa)
            all_aa.find(self.results_list_in_pocket[i][0][0][1])

            # coord[all_aa.find(self.results_list[i][0][1]):all_aa.find(self.results_list[i][0][1])+self.results_list[i][0][13]]==coord[all_aa.find(self.results_list[i][0][1]):all_aa.find(self.results_list[i][0][1])+self.results_list[i][0][13]]

            hcs_coord = coord[all_aa.find(self.results_list_in_pocket[i][0][0][1]):all_aa.find(
                self.results_list_in_pocket[i][0][0][1]) + self.results_list_in_pocket[i][0][0][13]]
            hcs_coord_flat_list = [item for sublist in hcs_coord for item in sublist]

            dist = np.linalg.norm(np.vstack([d for d in hcs_coord_flat_list]).max(axis=0) - np.vstack(
                [d for d in hcs_coord_flat_list]).min(axis=0))
            dist = math.ceil(dist)
            self.results_list_in_pocket[i][0][0].append(dist)

            appended = np.concatenate(hcs_coord_flat_list)
            wanted_array = np.reshape(appended, (-1, 3))
            box_center_coord = np.mean(wanted_array, axis=0)
            self.results_list_in_pocket[i][0][0].append(box_center_coord)

        return self.results_list_in_pocket

    def show_nglview(self):

        for i in range(len(self.results_list_in_pocket)):
            globals()[f"view{i}"] = nglview.show_pdbid(self.results_list_in_pocket[i][0][0][14])
            globals()[f"view{i}"].color_by("chainname")
            globals()[f"view{i}"].representations = [
                {"type": "ball+stick", "params": {
                    "sele": "protein", "color": "green"
                }},
                {"type": "ribbon", "params": {
                    "sele": f"{self.results_list_in_pocket[i][0][0][9]}-{self.results_list_in_pocket[i][0][0][10]}" + " and :" + f"{self.results_list_in_pocket[i][0][0][15]}",
                    "color": "blue"
                }}

            ]

            globals()[f"view{i}"].add_label(
                selection=f"{self.results_list_in_pocket[i][0][0][9]}-{self.results_list_in_pocket[i][0][0][10]}" + " and :" + f"{self.results_list_in_pocket[i][0][0][15]}")

            return (globals()[f"view{i}"])

    def do_docking_with_vina(self):

        # copy old ligand database in PDB

        os.chdir("./PDB")

        for i in range(len(self.results_list_in_pocket)):
            globals()[f"prepare_receptor{i}"] = ["obabel", "-ipdb", self.results_list_in_pocket[0][0][i][14] + ".pdb",
                                                 "-r", "-opdbqt", "-O",
                                                 self.results_list_in_pocket[0][0][i][14] + ".pdbqt"]
            subprocess.call(globals()[f"prepare_receptor{i}"])
            !grep ^ ATOM * {self.results_list_in_pocket[0][0][i][14] + ".pdbqt"} > {self.results_list_in_pocket[0][0][i][14] + "_cleaned.pdbqt"}

        for i in range(len(self.results_list_in_pocket)):
            for j in range(1, 36):
                globals()[f"docking_{i}_{j}"] = ["vina", "--receptor",
                                                 self.results_list_in_pocket[0][0][i][14] + "_cleaned.pdbqt",
                                                 "--ligand", f"viruses-fda_ligand_{j}.pdbqt", "--center_x",
                                                 str(self.results_list_in_pocket[0][0][i][19][0]), "--center_y",
                                                 str(self.results_list_in_pocket[0][0][i][19][1]), "--center_z",
                                                 str(self.results_list_in_pocket[0][0][i][19][2]), "--size_x",
                                                 str(self.results_list_in_pocket[0][0][i][18]), "--size_y",
                                                 str(self.results_list_in_pocket[0][0][i][18]), "--size_z",
                                                 str(self.results_list_in_pocket[0][0][i][18]), "--out",
                                                 self.results_list_in_pocket[0][0][i][
                                                     2] + "_" + f"viruses-fda{j}" + ".pdbqt", "--dir", "./"]
                subprocess.run(globals()[f"docking_{i}_{j}"])

    def parsing_docking_results(self):

        docking_result_list = []

        for i in range(len(self.results_list_in_pocket)):
            docking_result_file_list = !ls {self.results_list_in_pocket[0][0][i][2]}"_"viruses - fda *
            for j in range(len(docking_result_file_list)):
                docking_score = !grep - A1 "^MODEL 2" {docking_result_file_list[j]} | grep - v '^--' | tail - n1
                docking_score = "".join(docking_score)
                docking_result_list.append(
                    [docking_result_file_list[j].split("_")[0], docking_result_file_list[j].split("_")[2].split(".")[0],
                     docking_score])

        result_df = pd.DataFrame(np.nan, index=range(len(self.results_list_in_pocket) * 35),
                                 columns=["Receptor", "Ligand",
                                          "Affinity (kcal/mol)", "RMSD lower bound",
                                          "RMSD upper bound"])

        for i in range(len(docking_result_list)):
            result_df.loc[i, "Receptor"] = docking_result_list[i][0]
            result_df.loc[i, "Ligand"] = docking_result_list[i][1]
            result_df.loc[i, "Affinity (kcal/mol)"] = docking_result_list[i][2].split()[3]
            result_df.loc[i, "RMSD lower bound"] = docking_result_list[i][2].split()[4]
            result_df.loc[i, "RMSD upper bound"] = docking_result_list[i][2].split()[5]

        return result_df.sort_values(by="Affinity (kcal/mol)", ascending=False).head(3).reset_index(drop=True)
