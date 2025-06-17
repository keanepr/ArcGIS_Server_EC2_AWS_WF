
# Deep Learning with ArcGIS: Lightweight Environment & Troubleshooting Summary

## [OK] Project Goal
To run a deep learning notebook for bathymetric shipwreck detection on an AWS EC2 virtual desktop, with constrained disk space and a lightweight ArcGIS environment clone.

---

##  What Happened
### [WARNING] Disk Space Constraints
- The EC2 C: drive had <1 GB free at multiple points.
- Installing `deep-learning-essentials` failed repeatedly due to insufficient space.

### [OK] Lightweight Environment Decision
- Instead of using `conda install -c esri deep-learning-essentials` (~3.09 GB),
- We installed a lightweight version with:
  - `conda install -c esri arcgis`
  - `conda install pytorch torchvision torchaudio cpuonly -c pytorch`

---

## [FIX] Observed Errors
1. `ImportError: cannot import name 'MaskRCNN' from 'arcgis.learn'`
   - Cause: `MaskRCNN` requires `deep-learning-essentials`.
2. `ModuleNotFoundError: No module named 'fastai'`
   - Cause: Fastai was not included in the lightweight install.
3. `NameError: name 'rotate' is not defined`
   - Cause: `rotate` and related transforms are part of Fastai.
4. `NameError: name 'transforms' is not defined`
   - `transforms` was referenced before being defined.

---

## [STRATEGY] Strategy
- Ignored non-critical cells causing errors.
- Ran successful cells to retain notebook output.
- Deferred full model training and augmentation until more disk space is available.

---

## [ENV BACKUP] Conda Environment Management
- Created backup:
  ```
  conda activate arcgispro-py3-clone1-clean-gis-env
  conda list --explicit > arcgis-lite-env.txt
  move arcgis-lite-env.txt "%USERPROFILE%\Documents"
  ```
- To recreate:
  ```
  conda create --name arcgis-lite-clone --file arcgis-lite-env.txt
  conda activate arcgis-lite-clone
  ```

---


---

## [ANALYSIS] Additional Analysis: Conda Proswap Log

# Conda Proswap Log Analysis Summary

This summary analyzes the `conda_proswap.log` file and confirms the reduced functionality of the environment `arcgispro-py3-clone1-clean-gis-env`:


These entries validate our earlier discussion that the environment is functional, but intentionally stripped down to conserve space.