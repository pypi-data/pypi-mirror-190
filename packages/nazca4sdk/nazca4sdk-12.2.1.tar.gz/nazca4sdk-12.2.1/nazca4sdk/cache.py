"""Cache module"""
import json

import requests

from nazca4sdk.datahandling.open_data_client import OpenDataClient
from nazca4sdk.datahandling.hotstorage.variables_stats_info import VariableStatsInfo
from nazca4sdk.datahandling.hotstorage.variable_stats import VariablesStats
from nazca4sdk.datahandling.variable_historical_info import VariableHistoricalInfo
JSON_HEADERS = {'Content-Type': 'application/json',
                'Accept': 'application/json'}


class Cache:
    """
    System caching module to as a second layer of opendata with SDK
    """

    types_dict = {"IntegerT": "int", "Float32T": "float", "TimeT": "datetime",
                  "BooleanT": "bool", "StringT": "string", "UIntegerT": "int"}
    stats_variable_type = {"float", "int"}

    def __init__(self, https: bool = True):
        """
        Initializing opendata with HotStorage to receive system configuration

        """
        self._opendata = OpenDataClient(https)
        self._base_url = self._opendata.base_url
        self._types = {}
        self.modules = []
        self.variables = {}

    @property
    def load(self):
        """
        Loading definitions of modules and variables

        Returns:
            list: module_name list
            list: variable_name list

        """
        try:
            response = requests.get(
                f'{self._base_url}/api/Config/modulesDefinitions', verify=False)
            if response.status_code == 200:
                json_response = response.json()
                for element in json_response:
                    module = element['identifier']
                    self.modules.append(module)
                    definition_string = element['definition']
                    definition = json.loads(definition_string)
                    variables = definition["variables"]
                    variable_list = []
                    var_dict = {}
                    for variable in variables:
                        name = variable["name"]
                        variable_type = variable["type"]
                        variable_list.append(name)
                        try:
                            readable_variable_type = self.types_dict[variable_type]
                            var_dict[name] = readable_variable_type
                        except KeyError:
                            print(
                                f"Module {module} Variable {name} type {variable_type} not recognized!")
                    self.variables[module] = variable_list
                    self._types[module] = var_dict
                return True
            return False
        except requests.exceptions.ConnectionError:
            print("A Connection error occurred.")
            return False

    def read_historical_variable(self, variable_historical_info: VariableHistoricalInfo):
        """
        Get paged variables in specific time range

        Args:
            variable_historical_info: info about variable

        Returns:
            array of variable values : Paged Variable values from selected time range
        Example:
            read_historical_variable(variable_historical_info)
        """

        try:
            exist_vars = self.check_if_exist(variable_historical_info.module_name,
                                              variable_historical_info.variable_names)
            if not exist_vars:
                print(f"Module {variable_historical_info.module_name} or "
                      f"{variable_historical_info.variable_names} not exist")
                return None
            variables_grouped = self.check_variables(variable_historical_info.module_name,
                                                     variable_historical_info.variable_names)
            params = [
                ('module', variable_historical_info.module_name),
                ('startdate', variable_historical_info.start_date),
                ('enddate', variable_historical_info.end_date)
            ]

            for variable_type in variables_grouped:
                for variable_name in variable_type[1]:
                    params.append(
                        (f'groupedVariables[{variable_type[0]}]', variable_name))
            response = self._opendata.get_paged_data(url="/api/hotstorage/ReadHistoricalVariable",
                                                     params=params, page_size=variable_historical_info.page_size)
            return response
        except requests.exceptions.ConnectionError:
            print("Error - Get data from OpenData")
            return None

    def variable_over_day(self, module_name, variable_names, start_date, end_date):
        """
        Gets variable in specific time range by connection with open database

        Args:
            module_name - name of module,
            variable_names - list of variable names,
            start_time - beginning of the time range
            stop_time - ending of the time range

        Returns:
            DataFrame: values for selected variable and time range

        """

        try:
            exist_vars = self.check_if_exist(module_name, variable_names)
            if not exist_vars:
                print(f"Module {module_name} or {variable_names} not exist")
                return None
            variables_grouped = self.check_variables(
                module_name, variable_names)
            response = self._opendata.request_params(module_name=module_name,
                                                     grouped_variables=variables_grouped,
                                                     start_date=start_date,
                                                     end_date=end_date)
            return self._opendata.parse_response(response)
        except requests.exceptions.ConnectionError:
            print("Error - Get data from OpenData")
            return None

    def check_variables(self, module: str, variable: list):
        """Check variables type

        Args:
            module: module
            variable: list of variables

        Returns:
            List of tuples with variables grouped by type:
                [(type,[variables])]

        """

        grouped_variables = list(
            map(lambda x: [x, self._types[module][x]], variable))
        tables = set(map(lambda x: x[1], grouped_variables))
        variables_grouped = [
            (x, [y[0] for y in grouped_variables if y[1] == x]) for x in tables]
        return variables_grouped

    def check_if_exist(self, module: str, variables: list):
        """Verify if module or variable are in system

        Args:
            module:module
            variables:list of variables

        Returns:
            True(bool) if exists
            raise ArgumentMissing error if not exists

        """

        if module not in self._types:
            print(f'Module: {module} not found')
            return False
        for variable in variables:
            if variable not in self._types[module]:
                print(f'Variable: {variable} not found')
                return False

        return True

    def read_variables_stats(self, module: str, variables: [str], start_date: str, end_date: str):
        exist_vars = self.check_if_exist(module, variables)
        if not exist_vars:
            print(f"Module {module} or  variables {variables} not exist")
            return None
        variables_grouped = self.check_variables(module, variables)
        # check variables type
        for element in variables_grouped:
            if element[0] not in self.stats_variable_type:
                print("Variable to count stats should be type of:")
                for elemenet_type in self.stats_variable_type:
                    print(f" -  {elemenet_type}")
                print(f"Variables {element[1]} is type of {element[0]}")
                return None
        variables_stats_info = VariableStatsInfo(module=module, startDate=start_date, endDate=end_date,
                                                 variables=variables_grouped)
        response = self._opendata.read_variables_stats(variables_stats_info)
        if response.status_code == 200:
            variables_stats = VariablesStats.parse_raw(response.content)
            return variables_stats.stats()
        else:
            print("Error reading module variables stats")
            return []
