set_fml_appmode SEQ

# Compile the two designs
analyze -format sverilog -library spec {
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpu_bak/fpnew_pkg.sv
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpu_bak/registers.svh
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpu_bak/fpnew_top.sv
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpu_bak/fpnew_rounding.sv
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpu_bak/fpnew_opgroup_multifmt_slice.sv
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpu_bak/fpnew_opgroup_fmt_slice.sv
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpu_bak/fpnew_opgroup_block.sv
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpu_bak/fpnew_noncomp.sv
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpu_bak/fpnew_fma.sv
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpu_bak/fpnew_fma_multi.sv
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpu_bak/fpnew_divsqrt_th_32.sv
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpu_bak/fpnew_divsqrt_multi.sv
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpu_bak/fpnew_cast_multi.sv
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpu_bak/fpnew_classifier.sv
                                        }
                                        
analyze -format sverilog -library impl {
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpnew_pkg.sv
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/registers.svh
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpnew_top.sv
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpnew_rounding.sv
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpnew_opgroup_multifmt_slice.sv
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpnew_opgroup_fmt_slice.sv
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpnew_opgroup_block.sv
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpnew_noncomp.sv
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpnew_fma.sv
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpnew_fma_multi.sv
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpnew_divsqrt_th_32.sv
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpnew_divsqrt_multi.sv
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpnew_cast_multi.sv
                                        /home/autumn/vortex_verif/verif/new_cvfpu/src/fpnew_classifier.sv
                                        }

elaborate_seq -spectop fpnew_fma_multi -impltop fpnew_fma_multi

# Map inputs, outputs and blackboxes of the two design
map_by_name

## Create clock and reset signals
create_clock -period 100 spec.clk_i
create_reset spec.rst_ni -sense low

## Run reset simulation
sim_run -stable
sim_save_reset

#use SEQ config to map uninitialized registers
seq_config -extended_mapping -map_uninit -map_x zero 

# Run check command
check_fv 