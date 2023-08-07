
#set use_DDP = True; torchrun --nproc_per_node=4 demo.py
#set use_DDP = False: python demo.py

import comm_ddp_pkg.comm_ddp.comm as comm

use_DDP = False

if use_DDP:
    comm.launch_DDP()

# sometimes, you want every process to print their own statement
print(f'rank: {comm.get_local_rank()} - is it the main process()? -> {comm.is_main_process()}\n')

# sometimes, you're tired of seeing repeated info printed by different ranks.
comm.mprint(f'world_size: {comm.get_world_size()} -> this statement is printed by rank-{comm.get_local_rank()}')


if use_DDP:
    comm.cleanup()