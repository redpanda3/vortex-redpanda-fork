## Vortex On Openlane

This repo is under working. Forked from commit 8230b37. Vortex on openlane is to take less non-reccurent cost on ASIC proven of Vortex IP, by taping out through efabless 130 shuttles. Since each efabless shuttle is limited to 3.3*3.3 mm^2 of area, so some of this work is to explore the design space. We limit the targeted configuration as the following:

```
-DNUM_CLUSTERS=1 -DNUM_CORES=1 -DNUM_WARPS=1 -DNUM_THREADS=1 -DL1_DISABLE -DLMEM_DISABLE

```

The area is expected to be 0.6mm^2 per VX_core_top without considering utilizations.

Other part of work is to generate a VX_core_top that can be synthesized by yosys in openlane flow. We try the commercial tools, which gave no error. So we made a patch and verified by equivalent check.

An EAD(External Architecure Document) is appended under docs folder, includes config parameters, interface description of each module, and EAS(External Architecture Spec). They are for soc team to use. 

## Usage

To generate a VX_core_top that can be utilized in openlane flow is not so straight-forward(but quite simple in commercial EDA flow). Here is my receipe:

After building vortex, under build/hw/syn/yosys/build_VX_core_top

```
make
```

The synth.v is the targeted verilog modules that can be passed the openlane flow directly.

Changes are the Makefiles, I add a patch-yosys step to remove the unsynthesizable part.

Other changes are the modules in the third-parties, one main part is the retiming part such as (https://github.com/openhwgroup/cvfpu/blob/a6af691551ffbd76d5d9cf30774d3295a41615e4/src/fpnew_cast_multi.sv#L115):

```
  assign inp_pipe_operands_q[0] = operands_i;
  assign inp_pipe_is_boxed_q[0] = is_boxed_i;
  assign inp_pipe_rnd_mode_q[0] = rnd_mode_i;
  assign inp_pipe_op_q[0]       = op_i;
  assign inp_pipe_op_mod_q[0]   = op_mod_i;
  assign inp_pipe_src_fmt_q[0]  = src_fmt_i;
  assign inp_pipe_dst_fmt_q[0]  = dst_fmt_i;
  assign inp_pipe_int_fmt_q[0]  = int_fmt_i;
  assign inp_pipe_tag_q[0]      = tag_i;
  assign inp_pipe_mask_q[0]     = mask_i;
  assign inp_pipe_aux_q[0]      = aux_i;
  assign inp_pipe_valid_q[0]    = in_valid_i;
  // Input stage: Propagate pipeline ready signal to updtream circuitry
  assign in_ready_o = inp_pipe_ready[0];
  // Generate the register stages
  for (genvar i = 0; i < NUM_INP_REGS; i++) begin : gen_input_pipeline
    // Internal register enable for this stage
    logic reg_ena;
    // Determine the ready signal of the current stage - advance the pipeline:
    // 1. if the next stage is ready for our data
    // 2. if the next stage only holds a bubble (not valid) -> we can pop it
    assign inp_pipe_ready[i] = inp_pipe_ready[i+1] | ~inp_pipe_valid_q[i+1];
    // Valid: enabled by ready signal, synchronous clear with the flush signal
    `FFLARNC(inp_pipe_valid_q[i+1], inp_pipe_valid_q[i], inp_pipe_ready[i], flush_i, 1'b0, clk_i, rst_ni)
    // Enable register if pipleine ready and a valid data item is present
    assign reg_ena = (inp_pipe_ready[i] & inp_pipe_valid_q[i]) | reg_ena_i[i];
    // Generate the pipeline registers within the stages, use enable-registers
    `FFL(inp_pipe_operands_q[i+1], inp_pipe_operands_q[i], reg_ena, '0)
    `FFL(inp_pipe_is_boxed_q[i+1], inp_pipe_is_boxed_q[i], reg_ena, '0)
    `FFL(inp_pipe_rnd_mode_q[i+1], inp_pipe_rnd_mode_q[i], reg_ena, fpnew_pkg::RNE)
    `FFL(inp_pipe_op_q[i+1],       inp_pipe_op_q[i],       reg_ena, fpnew_pkg::FMADD)
    `FFL(inp_pipe_op_mod_q[i+1],   inp_pipe_op_mod_q[i],   reg_ena, '0)
    `FFL(inp_pipe_src_fmt_q[i+1],  inp_pipe_src_fmt_q[i],  reg_ena, fpnew_pkg::fp_format_e'(0))
    `FFL(inp_pipe_dst_fmt_q[i+1],  inp_pipe_dst_fmt_q[i],  reg_ena, fpnew_pkg::fp_format_e'(0))
    `FFL(inp_pipe_int_fmt_q[i+1],  inp_pipe_int_fmt_q[i],  reg_ena, fpnew_pkg::int_format_e'(0))
    `FFL(inp_pipe_tag_q[i+1],      inp_pipe_tag_q[i],      reg_ena, TagType'('0))
    `FFL(inp_pipe_mask_q[i+1],     inp_pipe_mask_q[i],     reg_ena, '0)
    `FFL(inp_pipe_aux_q[i+1],      inp_pipe_aux_q[i],      reg_ena, AuxType'('0))
  end
```

In the yosys, signal such as inp_pipe_operands_q[0] is already a wire, but inp_pipe_aux_q[i+1] is a register. I wrote an equivalent module for that and pass the seq formal verification(scritps are under hw/seq).

Another part is the the width of reg_ena_i signal, yosys cannot fully recognize that the reg_ena_i[-1] (https://github.com/openhwgroup/cvfpu/blob/a6af691551ffbd76d5d9cf30774d3295a41615e4/src/fpnew_cast_multi.sv#L63), this is a signal that forcely setup to zero but not effected, so I redefined it to 

```
input logic [ExtRegEnaWidth-1 + (ExtRegEnaWidth == 0? 1 : 0) :0]  reg_ena_i
```

To remove the unsed net, followed by this (https://github.com/YosysHQ/yosys/issues/94). Make sure to run 
hierarchy first. Those steps were included already in the yosys/Makefile by vortex original author Professor Blaise.

## Acknowledgement.

Thank you Professor Blaise and Vortex Group.


