## How to Run the Simulation


As mentioned in the README.md, the project is built by Makefile. Under vortex, 

```
make
```

The whole project is under vortex/build

### Run Simulation Under Simx or RTLsim

The performace modeling tool is called simx, to launch a demo, in vortex/build

```
./ci/blackbox.sh --driver=simx --app=lbm --warps=8
```

You will see the printed result of the test run. app refers to the app case under tests. If you want to add CONFIGS, for example, disable local memory, use
```
CONFIGS="-DLMEM_DISABLE" ./ci/blackbox.sh --driver=simx --app=lbm --warps=8
```

If you want to change to RTLsim, change the driver to rtlsim, for example

```
CONFIGS="-DLMEM_DISABLE" ./ci/blackbox.sh --driver=rtlsim --app=lbm --warps=8
```

In rtlsim driver, will generate a trace.vcd as waveform. If you have the verdi tool, it will be easier to use vcd2fsdb to convert to fsdb file and load the fsdb file. 


