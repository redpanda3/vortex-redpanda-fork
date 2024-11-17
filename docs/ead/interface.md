## VX_branch_ctl_if

branch control interface: alu or execute send schedule a bundle of branch control information. Since branch target result needs to be calculated by backend. 

```
valid bool: is this a branch
wid [NW_WIDTH-1:0]: warp id
taken bool: branch taken or not
dest [`PC_BITS-1:0]: branch destination

```

## VX_COMMIT_csr_of

From commit module to csr, and sfu. Send a piece of info of retired register count.

```
instret [`PERF_CTR_BITS-1:0]: The instret (Instructions Retired) register is a 44-bit register that holds the count of the number of instructions that have been retired, or in other words, completed execution. 
```

## VX_commit_if 

Commit info, the producer is the execution unit, consumer could be the trace unit within commit module, or gather unit

```
valid bool: valid of the payload
ready bool: ready of the payload
data_t.uuid [`UUID_WIDTH-1:0]: universal unique identifier
data_t.wid [`NW_WIDTH-1:0]: warp id
data_t.tmask [NUM_LANES-1:0]: mask value
data_t.pc [`PC_BITS-1:0]: program counter value
data_t.wb bool: write back to register or not
data_t.rd [`NR_BITS-1:0]: destination register 
data_t.data [NUM_LANES-1:0][`XLEN-1:0]: number of lanes of the data
data_t.pid [PID_WIDTH-1:0]: instance id within the threads.
data_t.sop bool: start of the operation.
data_t.eop bool: end of the operation.

```

## VX_commit_sched_if 

```
committed_warps [`NUM_WARPS-1:0]: whether this warp is committed
```

## VX_dcr_bus_if

Device configuration register bus

```
write_valid bool: device configuration write valid
write_addr [`VX_DCR_ADDR_WIDTH-1:0]: device configuration register address
write_addr [`VX_DCR_DATA_WIDTH-1:0]: device configuration register data
```

## VX_decode_if

From decode unit to execution unit

```
valid bool: valid of the payload
ready bool: ready of the payload
data_t.uuid [`UUID_WIDTH-1:0]: universal unique identifier
data_t.wid [NW_WIDTH-1:0]: warp id
data_t.tmask [`NUM_THREADS-1:0]: thread mask
data_t.pc [`PC_BITS-1:0]: program counter value
data_t.ex_type [`EX_BITS-1:0]: execution type: alu type, lsu type, fpu type or sfu type
data_t.op_type [`INST_OP_BITS-1:0]: operation type
data_t.op_args op_args_t : arguments for alu, fpu, lsu, csr, wctl
data_t.wb: write back to register or not
data_t.rd [`NR_BITS-1:0]: destination register 
data_t.rs1 [`NR_BITS-1:0]: source register 1
data_t.rs2 [`NR_BITS-1:0]: source register 2
data_t.rs3 [`NR_BITS-1:0]: source register 3

```

## VX_decode_sched_if

From decode unit to scheduler

```
valid bool: valid of the payload
is_wstall: need to be asked
wid [`NW_WIDTH-1:0]: warp id
```

## VX_dispatch_if 

infos from issue to dispatch

```
valid bool: valid of the payload
ready bool: ready of the payload
data_t.uuid [`UUID_WIDTH-1:0]: universal unique identifier
data_t.wis [ISSUE_WIS_W-1:0]: width of issue
data_t.tmask [`NUM_THREADS-1:0]: thread mask
data_t.PC [`PC_BITS-1:0]: program counter value
data_t.op_type [`INST_ALU_BITS-1:0]: operation type
data_t.op_args op_args_t : arguments for alu, fpu, lsu, csr, wctl
data_t.wb: write back to register or not
data_t.rd [`NR_BITS-1:0]: destination register 
data_t.tid [`NT_WIDTH-1:0]: thread id
data_t.rs1_data [`NUM_THREADS-1:0][`XLEN-1:0]: source register 1
data_t.rs2_data [`NUM_THREADS-1:0][`XLEN-1:0]: source register 2
data_t.rs3_data [`NUM_THREADS-1:0][`XLEN-1:0]: source register 3
```

## VX_execute_if


infos from dispatch to execute

```
valid bool: valid of the payload
ready bool: ready of the payload
data_t.uuid [`UUID_WIDTH-1:0]: universal unique identifier
data_t.wid [NW_WIDTH-1:0]: warp id
data_t.tmask [`NUM_THREADS-1:0]: thread mask
data_t.pc [`PC_BITS-1:0]: program counter value
data_t.op_type [`INST_OP_BITS-1:0]: operation type
data_t.op_args op_args_t : arguments for alu, fpu, lsu, csr, wctl
data_t.wb: write back to register or not
data_t.rd [`NR_BITS-1:0]: destination register 
data_t.tid [`NT_WIDTH-1:0]: thread id
data_t.rs1_data [NUM_LANES-1:0][`XLEN-1:0]: source register 1
data_t.rs2_data [NUM_LANES-1:0][`XLEN-1:0]: source register 2
data_t.rs3_data [`NUM_THREADS-1:0][`XLEN-1:0]: source register 3
data_t.pid [PID_WIDTH-1:0]: instance id within the threads
data_t.sop bool: start of the operation.
data_t.eop bool: end of the operation.
```

## VX_fetch_if

infos from fetch to decode

```
valid bool: valid of the payload
ready bool: ready of the payload
data_t.uuid [`UUID_WIDTH-1:0]: universal unique identifier
data_t.wid [NW_WIDTH-1:0]: warp id
data_t.tmask [`NUM_THREADS-1:0]: thread mask
data_t.pc [`PC_BITS-1:0]: program counter value
data_t.inst [31:0]: instruction

```

## VX_ibuffer_if

infos from instruction buffer to issue slice

```
valid bool: valid of the payload
ready bool: ready of the payload
data_t.uuid [`UUID_WIDTH-1:0]: universal unique identifier
data_t.tmask [`NUM_THREADS-1:0]: thread mask
data_t.pc [`PC_BITS-1:0]: program counter value
data_t.ex_type [`EX_BITS-1:0]: execution type: alu type, lsu type, fpu type or sfu 
data_t.op_type [`INST_OP_BITS-1:0]: operation type
data_t.op_args op_args_t : arguments for alu, fpu, lsu, csr, wctl
data_t.wb: write back to register or not
data_t.rd [`NR_BITS-1:0]: destination register 
data_t.rs1 [`NR_BITS-1:0]: source register 1
data_t.rs2 [`NR_BITS-1:0]: source register 2
data_t.rs3 [`NR_BITS-1:0]: source register 3
```

## VX_lsu_mem_if

infos from lsu unit to memory unit


request channel:

```
valid bool: valid of the payload
ready bool: ready of the payload
data_t.rw bool: read or write
data_t.mask [NUM_LANES-1:0]: mask value 
data_t.byteen [NUM_LANES-1:0][DATA_SIZE-1:0]: byte enable
data_t.addr [NUM_LANES-1:0][ADDR_WIDTH-1:0]: address
data_t.atype [NUM_LANES-1:0][ATYPE_WIDTH-1:0]: address type, default to be 1
data_t.data [NUM_LANES-1:0][DATA_SIZE*8-1:0]: data requested to store 
data_t.tag [TAG_WIDTH-1:0]: uuid+1?

```

responce channel:
```
valid bool: valid of the payload
ready bool: ready of the payload
data_t.mask [NUM_LANES-1:0]: mask value 
data_t.data [NUM_LANES-1:0][DATA_SIZE*8-1:0]: data requested to load
data_t.tag [TAG_WIDTH-1:0]: uuid+1?

```

## VX_operands_if

```
valid bool: valid of the payload
ready bool: ready of the payload
data_t.uuid [`UUID_WIDTH-1:0]: universal unique identifier
data_t.wis [ISSUE_WIS_W-1:0]: issue width
data_t.tmask [`NUM_THREADS-1:0]: thread mask
data_t.pc [`PC_BITS-1:0]: program counter value
data_t.ex_type [`EX_BITS-1:0]: execution type: alu type, lsu type, fpu type or sfu 
data_t.op_type [`INST_OP_BITS-1:0]: operation type
data_t.op_args op_args_t : arguments for alu, fpu, lsu, csr, wctl
data_t.wb: write back to register or not
data_t.rd [`NR_BITS-1:0]: destination register 
data_t.tid [`NT_WIDTH-1:0]: thread id
data_t.rs1_data [NUM_LANES-1:0][`XLEN-1:0]: source register 1
data_t.rs2_data [NUM_LANES-1:0][`XLEN-1:0]: source register 2
data_t.rs3_data [`NUM_THREADS-1:0][`XLEN-1:0]: source register 3

```

## VX_pipeline_perf_if

performance related interface

```
sched.idles [`PERF_CTR_BITS-1:0]: idles in scheduler
sched.stalls [`PERF_CTR_BITS-1:0]: stalls in scheduler
issue.ibf_stalls [`PERF_CTR_BITS-1:0]: stalls in sbuffer
issue.scb_stalls [`PERF_CTR_BITS-1:0]: stalls in scoreboard
issue.opd_stalls [`PERF_CTR_BITS-1:0]: stalls in operand
issue.units_uses [`NUM_EX_UNITS-1:0][`PERF_CTR_BITS-1:0]: unit uses in issues
issue.sfu_uses [`NUM_EX_UNITS-1:0][`PERF_CTR_BITS-1:0]: unit uses in sfu
ifetches [`PERF_CTR_BITS-1:0]: instruction fetched
loads  [`PERF_CTR_BITS-1:0]: loads count
store  [`PERF_CTR_BITS-1:0]: store count
ifetch_latency  [`PERF_CTR_BITS-1:0]: instruction fetch latency
load_latency  [`PERF_CTR_BITS-1:0]: load latency

```

## VX_sched_csr_if

From scheduler to csr register

```
cycles [`PERF_CTR_BITS-1:0]: cycles of busy in scheduler
active_warps [`NUM_WARPS-1:0]: number of active warps in scheduler
thread_masks [`NUM_WARPS-1:0][`NUM_THREADS-1:0]: thread masks of each warps
alm_empty bool: almost empty, means the scheduler has less than the almost threadthold of warps
alm_empty_wid [`NW_WIDTH-1:0]: warps that get almost empty 
unlock_warp bool: unlock the warp
unlock_wid [`NW_WIDTH-1:0]: unlock the corresponding warp id

```

## VX_scoreboad_if

```
valid bool: valid of the payload
ready bool: ready of the payload
data_t.uuid [`UUID_WIDTH-1:0]: universal unique identifier
data_t.tmask [`NUM_THREADS-1:0]: thread mask
data_t.pc [`PC_BITS-1:0]: program counter value
data_t.ex_type [`EX_BITS-1:0]: execution type: alu type, lsu type, fpu type or sfu 
data_t.op_type [`INST_OP_BITS-1:0]: operation type
data_t.op_args op_args_t : arguments for alu, fpu, lsu, csr, wctl
data_t.wb: write back to register or not
data_t.rd [`NR_BITS-1:0]: destination register 
data_t.rs1 [`NR_BITS-1:0]: source register 1
data_t.rs2 [`NR_BITS-1:0]: source register 2
data_t.rs3 [`NR_BITS-1:0]: source register 3

```

## VX_sfu_perf_if

```
wctl_stalls [`PERF_CTR_BITS-1:0]: no use
```

## VX_warp_ctl_if

warp control interface from execute to scheduler

```
valid bool: valid of the payload
wid [`NW_WIDTH-1:0]: warp id
tmc_t.valid bool: thread mask control valid
tmc_t.tmask [`NUM_THREADS-1:0]: active warp mask
wspawn_t.valid bool: warp spawn valid
wspawn_t.wmask [`NUM_WARPS-1:0] : mask to be setup
wspaen_t.pc [`PC_BITS-1:0]: program counter to be setup
split_t.valid bool: split mode
split_t.is_dvg bool: whether it is a divergent warp
split_t.then_tmask [`NUM_THREADS-1:0]: the mask of 'then'
split_t.else_tmask [`NUM_THREADS-1:0]: the mask of 'else'
split_t.next_pc [`PC_BITS-1:0]: next pc
join_t.valid bool: valid of payload
join_t.stack_ptr [`DV_STACK_SIZEW-1:0]: stack pointer
barrier_t.valid: valid of the payload
barrier_t.id [`NB_WIDTH-1:0]: barrier width
barrier_t.is_global bool: whether it is global barrier
barrier_t.is_noop: no operation
```

## VX_writeback_if

writeback interface from commit to issue

```
valid bool:valid of the payload
data_t.uuid [`UUID_WIDTH-1:0]: universal unique identifier
data_t.wis [ISSUE_WIS_W-1:0]: width of issue
data_t.tmask [`NUM_THREADS-1:0]: thread mask
data_t.PC [`PC_BITS-1:0]: program counter value
data_t.rd [`NR_BITS-1:0]: destination register 
data_t.tid [`NT_WIDTH-1:0]: thread id
data_t.data [NUM_LANES-1:0][`XLEN-1:0]: write back data
data_t.sop bool: start of the operation.
data_t.eop bool: end of the operation.
```

## VX_mem_bus_if


```
req_valid: the request is valid
req_ready: the consumer is ready

req_rw: 0 means the request is read type, 1 means the request is write type
req_byteen: byte enable, corresponds to the data, acts like a mask
req_addr: requested address
req_data: requested data
req_tag : addition infomations, for example, dbg uuid
req_flags : unused 

rsp_valid: the request is valid
rsp_ready: the consumer is ready

rsp_data: responded data
rsp_tag: rsp_uuid, rsp_wid, rsp_pc, rsp_wb, rsp_rd, rsp_op_type, rsp_align, rsp_pid, pkt_raddr, rsp_is_fence
```






































































