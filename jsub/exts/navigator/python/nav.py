#!/usr/bin/env python

import os
import sys
import re
import time
import getopt
import threading
import signal
import subprocess
import random

try:
    from Queue import Queue
except ImportError:
    from queue import Queue


################################################################################
# Utils

def mkdir_safe(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


################################################################################
# Setup the logger

import logging

jsub_logger = logging.getLogger('JSUB')
jsub_logger.setLevel(logging.DEBUG)

FORMATTER = logging.Formatter('[%(asctime)s][%(name)s|%(levelname)s]: %(message)s', '%Y-%m-%d %H:%M:%S UTC')
logging.Formatter.converter = time.gmtime

def add_stream_logger():
    logger = logging.getLogger('JSUB')

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(FORMATTER)

    logger.addHandler(ch)

def add_file_logger(log_root):
    logger = logging.getLogger('JSUB')

    mkdir_safe(log_root)
    log_file = os.path.join(log_root, 'navigator.log')

    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(FORMATTER)

    logger.addHandler(fh)
    logger.debug('='*80)

add_stream_logger()


################################################################################
# Parse arguments

class ArgParser:
    sub_roots = ['scenario', 'log', 'action', 'run', 'input', 'output']

    def __init__(self, argv):
        self.validation = False

        self.options = {}
        self.__argv = argv
        self.__parse_args()

    def __parse_args(self):
        long_opts = ['validate', 'task_sub_id=', 'main_root=']
        for sub_root in self.sub_roots:
            long_opts.append(sub_root + '_root=')

        opts, args = getopt.getopt(self.__argv, '', long_opts)
        for o, a in opts:
            self.options[o.lstrip('-')] = a

        if 'validate' in self.options:
            self.validation = True
            del self.options['validate']

        if 'main_root' not in self.options:
            self.options['main_root'] = '.'
        for sub_root in self.sub_roots:
            option_sub_root = sub_root + '_root'
            if option_sub_root not in self.options:
                self.options[option_sub_root] = os.path.join(self.options['main_root'], sub_root)

        self.options['scenario_file'] = os.path.join(self.options['scenario_root'], 'scenario.py')

    def read_scenario(self):
        scenario = {}

        jsub_logger.debug('Reading scenario from file: %s', self.options['scenario_file'])
        f = open(self.options['scenario_file'], 'r')
        try:
            scenario = eval(f.read())
        finally:
            f.close()

        scenario['general']['task_sub_id'] = self.options['task_sub_id']
        scenario['general']['main_root'] = self.options['main_root']

        for sub_root in self.sub_roots:
            option_sub_root = sub_root + '_root'
            scenario['general'][option_sub_root] = self.options[option_sub_root]

        scenario['general']['log_unit_root'] = os.path.join(self.options['log_root'], 'unit')
        mkdir_safe(scenario['general']['log_unit_root'])

        scenario['general']['input_common_dir'] = os.path.join(self.options['input_root'], 'common')
        scenario['general']['input_unit_root']  = os.path.join(self.options['input_root'], 'unit')

        return scenario


################################################################################
# Defining the DAG

class DAGVertexNotFoundError(Exception):
    pass

class DAGEdgeNotFoundError(Exception):
    pass

class DAGCycleError(Exception):
    pass


def dag_endpoints(graph):
    endpoints = set()
    for v_f, v_t in graph.items():
        if not v_t:
            endpoints.add(v_f)
    return endpoints

def dag_has_path_to(v_from, v_to, graph):
    if v_from == v_to:
        return True
    for v in graph[v_from]:
        if dag_has_path_to(v, v_to, graph):
            return True
    return False


class DAG:
    def __init__(self):
        self.__graph = {}
        self.__graph_reverse = {}


    def __validate_vertex(self, *vertice):
        for vertex in vertice:
            if vertex not in self.__graph:
                raise DAGVertexNotFoundError('Vertex "%s" does not belong to DAG' % vertex)


    def add_vertex(self, vertex):
        if vertex not in self.__graph:
            self.__graph[vertex] = set()
            self.__graph_reverse[vertex] = set()

    def add_edge(self, v_from, v_to):
        self.__validate_vertex(v_from, v_to)
        if dag_has_path_to(v_to, v_from, self.__graph):
            raise DAGCycleError('Cycle if add edge from "%s" to "%s"' % (v_from, v_to))

        self.__graph[v_from].add(v_to)
        self.__graph_reverse[v_to].add(v_from)

    def remove_edge(self, v_from, v_to):
        self.__validate_vertex(v_from, v_to)
        if v_to not in self.__graph[v_from]:
            raise DAGEdgeNotFoundError('Edge not found from "%s" to "%s"' % (v_from, v_to))

        self.__graph[v_from].remove(v_to)
        self.__graph_reverse[v_to].remove(v_from)


    def edge_size(self):
        size = 0
        for vertex in self.__graph:
            size += self.indegree(vertex)
        return size

    def successors(self, vertex):
        self.__validate_vertex(vertex)
        return set(self.__graph[vertex])

    def predecessors(self, vertex):
        self.__validate_vertex(vertex)
        return set(self.__graph_reverse[vertex])

    def indegree(self, vertex):
        self.__validate_vertex(vertex)
        return len(self.__graph_reverse[vertex])

    def outdegree(self, vertex):
        self.__validate_vertex(vertex)
        return len(self.__graph[vertex])

    def all_starts(self):
        return dag_endpoints(self.__graph_reverse)

    def all_terminals(self):
        return dag_endpoints(self.__graph)


################################################################################
# Run units

class UnitCannotRunError(Exception):
    pass


class UnitThread(threading.Thread):
    def __init__(self, queue_unit, unit, args, cwd, env, stdin):
        thread_name = 'Thread-' + unit
        threading.Thread.__init__(self, name=thread_name)

        self.__queue_unit = queue_unit
        self.__unit = unit
        self.__args = args
        self.__cwd = cwd
        self.__env = env
        self.__stdin = stdin

        self.__pid = 0
        self.__queue_pid = Queue()

        jsub_logger.debug('Execute unit: %s', self.__unit)
        jsub_logger.debug(' - args: %s', self.__args)
        jsub_logger.debug(' - cwd: %s', self.__cwd)
        jsub_logger.debug(' - env: %s', self.__env)
        jsub_logger.debug(' - stdin: %s', repr(self.__stdin))

    def run(self):
        stdout = ''
        stderr = ''
        returncode = None
        try:
            try:
                p = subprocess.Popen(args=self.__args, cwd=self.__cwd, env=self.__env,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                self.__queue_pid.put(p.pid)
                stdout, stderr = p.communicate(input=self.__stdin.encode())
                stdout = stdout.decode()
                stderr = stderr.decode()
                returncode = p.returncode
            except Exception:
                e = sys.exc_info()
                jsub_logger.exception('Thread "%s" exception (%s): %s' % (self.__unit, e[0].__name__, e[1]))
                self.__queue_pid.put(0)
        finally:
            self.__queue_unit.put({'unit': self.__unit, 'returncode': returncode, 'stdout': stdout, 'stderr': stderr})

    def unit_pid(self):
        self.__pid = self.__queue_pid.get()

    def terminate_unit(self):
        if self.__pid:
            os.kill(self.__pid, signal.SIGTERM)

    def kill_unit(self):
        if self.__pid:
            os.kill(self.__pid, signal.SIGKILL)


class UnitRunner:
    def __init__(self, scenario_general):
        self.__scenario_general = scenario_general
        self.__unit_threads = {}
        self.__queue_unit = Queue()

    def __args_basic(self, unit, action_type, executable):
        args = []
        args.append(os.path.join(self.__scenario_general['action_root'], action_type, executable))
        return args

    def __var_2_env(self, var):
        env = {}
        for k, v in var.items():
            env[k] = str(v)
        return env

    def __var_2_arg(self, var):
        args = []
        for k, v in var.items():
            args += ['--%s'%k, str(v)]
        return args

    def __var_2_stdin(self, var):
        stdin = ''
        for k, v in var.items():
            stdin += '%s=%s\n' % (k, str(v))
        return stdin

    def __find_pass_method(self, pass_method, method):
        method_fragments = method.split('+')
        if pass_method in method_fragments:
            return method_fragments
        return []

    def __generate_sub_var(self, pass_method, method_fragments, var_data):
        var = {}
        for k, v in var_data.items():
            var_name = ''
            for frag in method_fragments:
                if frag == pass_method:
                    var_name += k
                else:
                    var_name += frag
            var[var_name] = v
        return var

    def __generate_var(self, pass_method, data):
        var = {}
        pass_var = data['param']['pass_var']
        for var_type, methods in pass_var.items():
            for method in methods:
                method_fragments = self.__find_pass_method(pass_method, method)
                if method_fragments:
                    var.update(self.__generate_sub_var(pass_method, method_fragments, data[var_type]))
        return var

    def __start_unit(self, unit, data):
        # generate all variables
        var_env  = self.__generate_var('env',  data)
        var_arg  = self.__generate_var('arg',  data)
        var_pipe = self.__generate_var('pipe', data)

        jsub_logger.debug('Variables for unit "%s":', unit)
        jsub_logger.debug(' - Passed by env: %s', var_env)
        jsub_logger.debug(' - Passed by arg: %s', var_arg)
        jsub_logger.debug(' - Passed by pipe: %s', var_pipe)

        # generate args for UnitThread
        args_basic = self.__args_basic(unit, data['type'], data['param']['executable'])
        args_var   = self.__var_2_arg(var_arg)
        args = args_basic + args_var

        cwd = data['sysvar']['run_dir']

        env = os.environ.copy()
        env.update(self.__var_2_env(var_env))

        stdin = self.__var_2_stdin(var_pipe)

        # create thread for a unit
        mkdir_safe(data['sysvar']['run_dir'])
        mkdir_safe(data['sysvar']['log_dir'])
        self.__unit_threads[unit] = UnitThread(self.__queue_unit, unit, args, cwd, env, stdin)
        self.__unit_threads[unit].start()
        self.__unit_threads[unit].unit_pid()

    def start_units(self, data_units):
        for unit, data in data_units.items():
            if unit in self.__unit_threads:
                jsub_logger.debug('Skip starting unit "%s", already running', unit)
                continue
            self.__start_unit(unit, data)


    def __analyze_jsub_outvar(self, stdout):
        var = {}
        r = re.compile('^[ \t]*JSUB_([A-Z]+)_(\w+)[ \t]*=[ \t]*(.*)[ \t]*$', flags=re.MULTILINE)
        for m in r.finditer(stdout):
            var_type = m.group(1).lower()
            jsub_logger.debug('Find jsub %s variable: %s', var_type, m.groups())
            if var_type not in var:
                var[var_type] = {}
            var[var_type][m.group(2)] = m.group(3)
        return var

    def __wait_finished_unit(self, timeout=None):
        item = self.__queue_unit.get(timeout=timeout)
        unit = item['unit']

        jsub_logger.info('Unit "%s" finished with exit code: %s', unit, item['returncode'])
        jsub_logger.debug((' - Standard output:\n%s' % item['stdout']).rstrip('\n'))
        jsub_logger.debug((' - Standard error:\n%s' % item['stderr']).rstrip('\n'))

        return item

    def __finished_unit(self):
        result = self.__wait_finished_unit()
        unit = result['unit']
        outvar = self.__analyze_jsub_outvar(result['stdout'])

        for var_type, var in outvar.items():
            for k, v in var.items():
                jsub_logger.info('Unit "%s" %s: %s = %s', unit, var_type, k, v)

        unit_info = result
        unit_info['outvar'] = outvar
        return unit_info

    def finished_units(self):
        units = {}
        if self.__unit_threads:
            unit_info = self.__finished_unit()
            unit = unit_info['unit']

            self.__unit_threads[unit].join()
            del self.__unit_threads[unit]

            units[unit] = unit_info
        return units


    def kill_all_units(self):
        killed_units = {}

        for unit, unit_thread in self.__unit_threads.items():
            unit_thread.terminate_unit()
        while self.__unit_threads:
            try:
                result = self.__wait_finished_unit(30)
            except Queue.Empty:
                break
            unit = result['unit']
            self.__unit_threads[unit].join()
            del self.__unit_threads[unit]
            killed_units[unit] = result

        # try to kill process if it cannot be terminated
        for unit, unit_thread in self.__unit_threads.items():
            unit_thread.kill_unit()
        while self.__unit_threads:
            try:
                result = self.__wait_finished_unit(5)
            except Queue.Empty:
                for unit in list(self.__unit_threads):
                    del self.__unit_threads[unit]
                    killed_units[unit] = -1
                break
            unit = result['unit']
            self.__unit_threads[unit].join()
            del self.__unit_threads[unit]
            killed_units[unit] = result

        return killed_units


class TaskSubIdNotFoundError(Exception):
    pass


class Application:
    def __init__(self, scenario):
        self.__scenario_general  = scenario['general']

        task_sub_id = self.__scenario_general['task_sub_id']
        all_jobvar = scenario['jobvar']
        if task_sub_id not in all_jobvar:
            raise TaskSubIdNotFoundError('Task sub ID not found: %s', task_sub_id)
        self.__scenario_jobvar   = all_jobvar[task_sub_id]

        self.__scenario_workflow = scenario['workflow']
        self.__scenario_event    = scenario['event']

        self.__data_workflow = {}
        for unit in self.__scenario_workflow:
            self.__data_workflow[unit] = {}
            self.__data_workflow[unit]['sysvar'] = self.__init_sysvar(unit)
            self.__data_workflow[unit]['jobvar'] = self.__scenario_jobvar
            self.__data_workflow[unit]['actvar'] = self.__scenario_workflow[unit]['actvar']
            self.__data_workflow[unit]['depvar'] = {}
            self.__data_workflow[unit]['type'] = self.__scenario_workflow[unit]['type']
            self.__data_workflow[unit]['param'] = self.__scenario_workflow[unit]['param']

        self.__unit_runner = UnitRunner(self.__scenario_general)

    def __init_sysvar(self, unit):
        sysvar = self.__scenario_general.copy()
        sysvar['unit'] = unit
        sysvar['log_dir'] = os.path.join(self.__scenario_general['log_unit_root'], unit)
        sysvar['run_dir'] = os.path.join(self.__scenario_general['run_root'], unit)
        sysvar['input_dir'] = os.path.join(self.__scenario_general['input_unit_root'], unit)
        return sysvar


    def run(self):
        self.generate_dag()
        self.execute_dag()

    def generate_dag(self):
        dag = DAG()
        for unit in self.__scenario_workflow:
            dag.add_vertex(unit)
        for unit, scenario_unit in self.__scenario_workflow.items():
            for unit_from in scenario_unit.get('depend_on', []):
                jsub_logger.debug('Add direction for DAG: %s -> %s', unit_from, unit)
                dag.add_edge(unit_from, unit)
        self.__dag_workflow = dag

    def execute_dag(self):
        # units with zero indegree are ready to be executed
        vertice_zero_indegree = self.__dag_workflow.all_starts()
        jsub_logger.debug('Initial unit(s) with zero indegree: %s', vertice_zero_indegree)

        while vertice_zero_indegree:
            data_units = {}
            for unit in vertice_zero_indegree:
                data_units[unit] = self.__data_workflow[unit]

            self.__unit_runner.start_units(data_units)
            units_info = self.__unit_runner.finished_units()
            jsub_logger.debug('Current unit (%s) -> Finished unit (%s)', vertice_zero_indegree, units_info.keys())

            if not units_info:
                raise UnitCannotRunError('No unit could run: %s', vertice_zero_indegree)

            for unit, info in units_info.items():
                vertice_zero_indegree.remove(unit)

                for to_unit in self.__dag_workflow.successors(unit):
#                    self.__data_workflow[to_unit]['depvar'].update(self.__data_workflow[unit]['depvar'])
                    if 'depvar' in info['outvar']:
                        self.__data_workflow[to_unit]['depvar'].update(info['outvar']['depvar'])

                    self.__dag_workflow.remove_edge(unit, to_unit)
                    if self.__dag_workflow.indegree(to_unit) == 0:
                        vertice_zero_indegree.add(to_unit)


################################################################################
# Main

def validate_navigator_env():
    print('JSUB navigator OK')
    return True

def main():
    try:
        arg_parser = ArgParser(sys.argv[1:])

        if arg_parser.validation:
            if validate_navigator_env():
                return 0
            else:
                return 1

        options = arg_parser.options
        add_file_logger(options['log_root'])
        jsub_logger.debug('Parse arguments to options: %s', options)

        scenario = arg_parser.read_scenario()
        jsub_logger.debug('Read scenario: %s', scenario)

        app = Application(scenario)
        app.run()
    except Exception:
        e = sys.exc_info()
        jsub_logger.exception('Exception caught (%s): %s' % (e[0].__name__, e[1]))
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
