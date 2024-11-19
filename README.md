## Vortex On Openlane

This repo is under working. Forked from commit 8230b37. Vortex on openlane is to take less non-reccurent cost on ASIC proven of Vortex IP, by taping out through efabless 130 shuttles. Since each efabless shuttle is limited to 3.3*3.3 mm^2 of area, so some of this work is to explore the design space. We limit the targeted configuration as the following:

```
-DNUM_CLUSTERS=1 -DNUM_CORES=1 -DNUM_WARPS=1 -DNUM_THREADS=1 -DL1_DISABLE -DLMEM_DISABLE

```

The area is expected to be 0.6mm^2 per VX_core_top without considering utilizations.

Other part of work is to generate a VX_core_top that can be synthesized by yosys in openlane flow. We try the commercial tools, which gave no error. So we made a patch and verified by equivalent check.

An EAD(External Architecure Document) is appended under docs folder, includes config parameters, interface description of each module, and EAS(External Architecture Spec). They are for soc team to use. 