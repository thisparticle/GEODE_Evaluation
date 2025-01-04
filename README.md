This GitHub repository contains configuration files for several open-source algorithms adapted to the GEODE dataset. We made minimal modifications to the open-source algorithms, which include necessary changes for compatibility with the Ubuntu 20.04 system and the implementation of TUM trajectory-saving code.  

### Procedure for obtaining results on the GEODE dataset:

1. **Benchmarking and Testing**:  
   All algorithms were tested using five independent runs. The average Absolute Trajectory Error (ATE) across these runs was reported in the benchmark table.  

2. **Parameter Tuning**:  
   We initially adjusted the sensor parameters to fit the GEODE dataset using the configuration files provided by the open-source algorithms. If significant drift occurred, minimal over-parameterization was applied to maintain valid trajectory outputs. If multiple parameter adjustments failed to produce meaningful results, the method was considered unsuccessful on the respective sequence.  

3. **Handling Divergent Results**:  
   During the five independent runs, some algorithms produced only a few successful localizations for specific sequences, while the remaining runs resulted in significant drift and failed to generate meaningful trajectories. To reflect the optimal performance of the algorithms, we excluded these divergent results from the reported averages.  

4. **Modifications for LVI-SAM**:  
   Since the official LVI-SAM code hardcoded multi-sensor coordinate transformations that were not configurable, we utilized a [third-party version](https://github.com/Cc19245/LVI-SAM-Easyused) with modified coordinate transformations. These modifications were solely for enabling compatibility with our dataset and did not influence the algorithm's performance.  

---

### Steps to reproduce our results:

1. Clone this repository, configure the environment as outlined in the corresponding code's README documentation, and then use `catkin build` to compile the workspace.  

2. Prepare the [GEODE dataset](https://github.com/PengYu-Team/GEODE_dataset). Update the dataset path and TUM trajectory output path in the `test_geode.py` script, and then execute the script.  

3. Follow the error evaluation instructions in the GEODE dataset's README to calculate errors.
