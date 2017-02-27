from node_function_manager import NodeFunctionManager

fid = 'a49b1ab2b9291945'
nfm = NodeFunctionManager()

# load
directory = nfm.load(fid)

# run
image_name, port, container_id = nfm.run(fid, directory)

# stop
nfm.stop(container_id, directory)
