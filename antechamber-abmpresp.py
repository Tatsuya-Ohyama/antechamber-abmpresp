#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Program to replace atom charge with ABINITMP RESP charge
"""

import sys, signal
sys.dont_write_bytecode = True
signal.signal(signal.SIGINT, signal.SIG_DFL)

import parmed
import subprocess
import os

from mods.func_prompt_io import check_exist



# =============== function =============== #
def parse_argument(list_arg):
	"""
	Function to parse arguments

	Args:
		list_arg (list): arguments

	Returns:
		str: ABINIT-MP log file
		dict: {option(str): value(str), ...}
	"""
	dict_arg = {}
	prev_arg = None
	flag_overwrite = False
	for arg in list_arg:
		if arg == "-L":
			exec_antechamber({"-L": None})
			sys.exit(0)

		elif arg == "--help" or arg == "-h":
			exec_antechamber({})
			show_help()
			sys.exit(0)

		elif arg.startswith("-"):
			dict_arg[arg] = None
			prev_arg = arg

		else:
			dict_arg[prev_arg] = arg

	log_file = None
	if "-il" in dict_arg.keys():
		log_file = dict_arg["-il"]
		del(dict_arg["-il"])

	else:
		sys.stderr.write("ERROR: ABINIT-MP log file is not specified.\n")
		sys.exit(1)

	return log_file, dict_arg, flag_overwrite


def read_log(input_file):
	"""
	Function to read ABINIT-MP log file and get atom charges

	Args:
		input_file (str): ABINIT-MP log file

	Returns:
		list: [charge(float), ...]
	"""
	list_charge = []
	with open(input_file, "r") as obj_input:
		flag_read = 0
		for line_val in obj_input:
			if "## ESP-FITTING TYPE:" in line_val:
				flag_read += 1
				continue

			if flag_read and "---------" in line_val:
				flag_read += 1
				continue

			if flag_read == 3:
				line_val = line_val.strip()
				if len(line_val) == 0:
					break

				elems = line_val.split()
				list_charge.append(float(elems[4]))

	return list_charge


def exec_antechamber(dict_arg):
	"""
	Function to execute `antechamber`

	Args:
		dict_arg (dict): arguments
	"""
	list_arg = ["antechamber"]
	for k, v in dict_arg.items():
		list_arg.append(k)
		if v is None:
			continue
		list_arg.append(v)

	obj_proc = subprocess.Popen(list_arg, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
	print(obj_proc.communicate()[0])


def write_mol2(mol2_file, list_charge):
	"""
	Function to modify charge in .mol2

	Args:
		mol2_file (str): .mol2 file
		list_charge (list): [charge(float), ...]
		flag_overwrite (bool): overwrite forcibly
	"""
	obj_mol = None
	obj_mol = parmed.load_file(mol2_file, structure=True)

	for obj_atom, charge in zip(obj_mol.atoms, list_charge):
		obj_atom.charge = charge

	obj_mol.save(mol2_file, overwrite=True)


def show_help():
	"""
	Function to show help for this wrapper program
	"""
	sys.stderr.write("                   -il ABINIT-MP.log     ABINIT-MP .log file\n")



# =============== main =============== #
if __name__ == '__main__':
	log_file, dict_arg, flag_overwrite = parse_argument(sys.argv[1:])
	dict_arg["-c"] = "gas"
	if os.path.splitext(dict_arg["-o"])[1] != ".mol2":
		sys.stderr.write("ERROR: output is not .mol2 file.\n")
		sys.exit(1)

	check_exist(log_file, 2)
	list_charge = read_log(log_file)

	exec_antechamber(dict_arg)

	write_mol2(dict_arg["-o"], list_charge)
