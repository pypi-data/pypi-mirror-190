from node import Node
import copy

class Network():
    
    def __init__(self, pre_build_network: dict = None) -> None:
        self.used_alias: dict[str:int] = {}
        self.aliases: dict[str:str] = {}
        if pre_build_network:
            network = self.setup_prebuild_network(pre_build_network)
            if network:
                self.network: dict[str: Node] = network
                return
        self.network: dict[str: Node] = {}

    def add_node(self, name, dependencies:set = set(), dependents: set = set(), create_unexisting_dep = False):
        
        if dependencies.intersection(dependents) or name in dependents or name in dependencies:
            raise ValueError("Bucle reference on network not allowed.")
        
        if name in self.aliases:
            raise ValueError("Unable to add node with this name since it already exists in the network")

        alias = self._find_free_alias(name) #Register new alias
        self.aliases[name] = alias
        if dependencies:
            for dep_i in dependencies:
                if dep_i not in self.aliases:
                    if create_unexisting_dep:
                        self.add_node(dep_i)
                    else:
                        raise ValueError(f"Couldnt find the dependencie node named={dep_i}")

        if dependents:
            for dep_i in dependents:
                if dep_i not in self.aliases:
                    if create_unexisting_dep:
                        self.add_node(dep_i, dependencies={name})
                    else:
                        raise ValueError(f"Couldnt find the dependencie node named={dep_i}")
                else:
                    self.network[self.aliases.get(dep_i)].dependencies.add(name)
        network = copy.deepcopy(self.network)
        network[alias] = Node(name, dependencies)
        non_bucle = self._find_bucle_reference_on_network(network)
        if not non_bucle:
            raise ValueError("Bucle reference on network not allowed.")
        
        self.network[alias] = Node(name, dependencies)
        
    def _find_free_alias(self, name):
        """Must use right before adding a node to network. In case of no addind the node please use remove alias, otherwise it might lead to unkown behaviour or dict key errors on network. 

        Args:
            name (str): Name of the new node that wants to be reduced to an alias that will be stored as key in network dictionary. 

        Returns:
            str: Alias
        """
        letter = name[0].upper()
        if not letter in self.used_alias:
            self.used_alias[letter] = 1
            return letter

        alias = f"{letter}{self.used_alias[letter]}"
        self.used_alias[letter] += 1
        
        return alias
    
    def _find_bucle_reference_on_network(self, network):
        
        def _recursive_bucle_reference_sercher(network: dict[str:Node], alias:str, trace: set):
            node = network.get(self.aliases.get(alias))
            trace.add(node.name)
            if trace.intersection(node.dependencies):
                return False, trace

            restantes = list(node.dependencies.difference(trace))
            non_bucle = True
            new_checked = set()

            while non_bucle and len(restantes)>0:
                non_bucle, checked = _recursive_bucle_reference_sercher(network, restantes[0], trace)

                for ch_i in checked:
                    if ch_i in restantes:
                        restantes.remove(ch_i)
                    else:
                        if ch_i is not alias:
                            new_checked.add(ch_i)
                    
            trace = trace.union(node.dependencies).union(new_checked)
            return non_bucle, trace
        
        elements = [n.name for _, n in network.items()]
        non_bucle = True
        while len(elements)>0 and non_bucle:
            alias = elements[0]
            non_bucle, checked = _recursive_bucle_reference_sercher(network, alias, set())
            for r in checked:
                if r in elements:
                    elements.remove(r)
        return non_bucle
            
    def setup_prebuild_network(self, pre_build_network: dict):
        reverse_network: dict[str:set]= {}
        origin = set()
        destination = set()
        for name_i in pre_build_network:
            if name_i not in self.aliases:
                alias = self._find_free_alias(name_i)
                self.aliases[name_i] = alias
                origin.add(name_i)
                reverse_network[name_i] = set()
            for related_i in pre_build_network.get(name_i):
                if related_i not in self.aliases:
                    alias = self._find_free_alias(related_i)
                    self.aliases[related_i] = alias
                    destination.add(related_i)
                    reverse_network[related_i] = {name_i}
                else:
                    reverse_network[related_i].add(name_i)
        network = {}
        for net_i, dependencies in reverse_network.items():
            network[self.aliases.get(net_i)] = Node(net_i, dependencies)   
 
        non_bucle = self._find_bucle_reference_on_network(network)

        if not non_bucle:
            raise ValueError("Bucle reference on network not allowed.")
        
        return network