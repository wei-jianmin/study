truct private_kernel_interface_t {
	// Public part of kernel_interface_t object 
	kernel_interface_t public;
	// Registered IPsec constructor 
	kernel_ipsec_constructor_t ipsec_constructor;
	// Registered net constructor 
	kernel_net_constructor_t net_constructor;
	// ipsec interface 
	kernel_ipsec_t *ipsec;
	// network interface 
	kernel_net_t *net;
	// mutex for listeners 
	mutex_t *mutex;
	// list of registered listeners 
	linked_list_t *listeners;
	// Reqid entries indexed by reqids 
	hashtable_t *reqids;
	// Reqid entries indexed by traffic selectors 
	hashtable_t *reqids_by_ts;
	// mutex for algorithm mappings 
	mutex_t *mutex_algs;
	// List of algorithm mappings (kernel_algorithm_t*) 
	linked_list_t *algorithms;
	// List of interface names to include or exclude (char*)
    // NULL if interfaces are not filtered 
	linked_list_t *ifaces_filter;
	// TRUE to exclude interfaces listed in ifaces_filter, 
    // FALSE to consider only those listed there 
	bool ifaces_exclude;
};
