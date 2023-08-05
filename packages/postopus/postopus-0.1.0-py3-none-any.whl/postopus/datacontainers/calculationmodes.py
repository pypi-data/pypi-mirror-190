import pathlib
from typing import Dict, List, Tuple, Union

import pandas as pd

from postopus.datacontainers.field import ScalarField, TDGeneralVectorField, VectorField
from postopus.datacontainers.util.convenience_dict import ConvenienceDict
from postopus.datacontainers.util.special_characters import (
    handle_fields_special_chatacters,
)
from postopus.files import openfile


class CalculationModes(ConvenienceDict):
    # Set name of dict in ConvenienceDict
    __dict_name__ = "fields"

    def __init__(
        self,
        mode: str,
        fields_in_mode: Dict[
            str, Union[Tuple[str, List[str]], List[pathlib.Path], List[str]]
        ],
        systemdir: str,
        systemname: str,
    ) -> None:
        """
        Class that build a dict of all fields present in a system for a given
        CalculationMode output.

        Parameters
        ----------
        mode : str
            Name of the calculation mode in the output. Naming like in Octopus'
            output (e. g. 'td', 'scf', ...)
        fields_in_mode : dict
            fields contained in the given calculation mode for this system
        systemdir : str
            directory in the filesystem which contains the output (folder 'output_iter')
            for one of the simulated systems in a run with Octopus
        systemname : str
            Name of the system, as found in OutputCollector.

        """
        # Init system dict in super
        super().__init__()

        self.mode = mode
        try:
            self._containingfields = fields_in_mode["fields"]
        except KeyError:
            # This happend, if we have a folder "static" or "td.general", but no fields
            # were written out to "output_iter". Example inp for this is benzene
            self._containingfields = []

        self.fields = {}
        for field in self._containingfields:
            # self.fields is available through ConvenienceDict

            # Scalar fields are written to a single file, vector fields are stored in
            # three files, consisting of the field name and a suffix '-[xyz]'.
            # self.fields keys should only be the field names, for vector fields the
            # suffix should be removed. Vector field orientation then is accessible
            # via e. g. 'self.field_name.x' for 'x' direction.

            # Find scalar fields
            # the dashes are replaced by underscores, since they are a special char.
            dimension_keys = ("-x", "-y", "-z")
            # next line is a glorified OR operation, if one of the keys exists. If so,
            # we have a vector field, otherwise it's scalar.
            if field.endswith(dimension_keys):
                fieldaccessor = field[:-2]
                if (
                    handle_fields_special_chatacters(fieldaccessor)
                    in self.fields.keys()
                ):
                    continue
                self.fields[
                    handle_fields_special_chatacters(fieldaccessor)
                ] = VectorField(
                    fieldaccessor,
                    systemdir,
                    systemname,
                    self.mode,
                    fields_in_mode,
                )
            else:
                self.fields[handle_fields_special_chatacters(field)] = ScalarField(
                    field,
                    systemdir,
                    systemname,
                    self.mode,
                    fields_in_mode,
                )

        # Some CalculationModes have special outputs, e. g. 'gs' writes stuff like
        # 'info', 'eigenvalues', 'convergence' or 'forces' into a folder 'static'.
        # 'td' produces a folder 'td.general' per system with outputs like 'laser',
        # 'multipoles' or 'energy'. These files do not have a suffix. We use this for
        # identification of such files.
        if mode == "scf":
            if "static" in fields_in_mode:
                for sf in fields_in_mode["static"]:
                    _fileobj = openfile(sf)
                    self.fields[sf.name] = _fileobj.values
                    if type(self.fields[sf.name]) == pd.DataFrame:
                        self.fields[sf.name].attrs = _fileobj.attrs

        if mode == "td":
            if "tdgeneral" in fields_in_mode:
                for tf in fields_in_mode["tdgeneral"]:
                    # Vector fields in td.general
                    if tf.name.endswith(("_x", "_y", "_z")):
                        vfield_name = tf.name[:-2]
                        if vfield_name in self.fields:
                            continue
                        self.fields[vfield_name] = TDGeneralVectorField(
                            vfield_name, fields_in_mode["tdgeneral"]
                        )
                    # Scalar fields in td.general
                    else:
                        _fileobj = openfile(tf)
                        self.fields[tf.name] = _fileobj.values
                        # Adding units attribute, NOT a column of the dataframe.
                        self.fields[tf.name].attrs = _fileobj.attrs
